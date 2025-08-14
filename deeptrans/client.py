import aiohttp
import asyncio
from typing import Union, List, Optional, Dict, Any

from deeptrans.exceptions import (
    DeepLException,
    AuthorizationException,
    QuotaExceededException,
    TooManyRequestsException
)

from deeptrans.constants import (
    LANGCODES, SOURCE_LANGCODES,
    LANGKEYS, SOURCE_LANGKEYS,
    LANGNAMES, SOURCE_LANGNAMES,
)

from deeptrans.models import (
    Formality,
    SplitSentences,
    ModelType,
    TextResult,
    Usage,
    Language
)


class AsyncDeepLClient:
    """
    Asynchronous DeepL API client for text translations.
    
    Args:
        auth_key (str): Your DeepL API authentication key.
        server_url (str, optional): Custom server URL. If None, automatically detects free/pro.
        session (aiohttp.ClientSession, optional): Custom aiohttp session. If None, creates internal session.
        max_retries (int): Maximum number of retries for failed requests. Default: 5.
        timeout (int): Request timeout in seconds. Default: 2.
    """
    
    _DEEPL_SERVER_URL = "https://api.deepl.com"
    _DEEPL_SERVER_URL_FREE = "https://api-free.deepl.com"
    _HTTP_STATUS_QUOTA_EXCEEDED = 456
    
    def __init__(
        self,
        auth_key: str,
        *,
        server_url: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        max_retries: int = 5,
        timeout: int = 2
    ):
        if not auth_key:
            raise ValueError("auth_key must not be empty")
            
        self.auth_key = auth_key
        self._own_session = session is None
        self._session = session
        self.max_retries = max_retries
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        
        # Auto-detect server URL based on auth key
        if server_url is None:
            server_url = (
                self._DEEPL_SERVER_URL_FREE
                if self._is_free_account(auth_key)
                else self._DEEPL_SERVER_URL
            )
        self.server_url = server_url.rstrip('/')
        
        self.headers = {
            "Authorization": f"DeepL-Auth-Key {auth_key}",
            "Content-Type": "application/json",
            "User-Agent": "deepl-python-async/1.0.0"
        }
    
    @staticmethod
    def _is_free_account(auth_key: str) -> bool:
        """Check if the auth key belongs to a free account."""
        return auth_key.endswith(":fx")
    
    async def __aenter__(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the aiohttp session if it was created internally."""
        if self._own_session and self._session:
            await self._session.close()
            self._session = None
    
    def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
            self._own_session = True
        return self._session
    
    async def _make_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """Make an HTTP request to the DeepL API with retries."""
        url = f"{self.server_url}/{endpoint.lstrip('/')}"
        session = self._get_session()
        
        if "languages" in endpoint and method == "GET" :
            try:
                del self.headers["Content-Type"]  # GET requests do not need Content-Type
            except :
                pass
        
        for attempt in range(self.max_retries + 1):
            try:
                async with session.request(
                    method,
                    url,
                    json=data if data else None,
                    headers=self.headers
                ) as response:
                    content = await response.text()
                    
                    # Handle different HTTP status codes
                    if response.status == 200:
                        try:
                            return await response.json()
                        except aiohttp.ContentTypeError:
                            return {"text": content}
                    
                    elif response.status == 401:
                        raise AuthorizationException(
                            "Invalid authentication key",
                            http_status_code=response.status
                        )
                    
                    elif response.status == 403:
                        raise AuthorizationException(
                            "Authorization failed, please check your authentication key",
                            http_status_code=response.status
                        )
                    
                    elif response.status == 404:
                        raise DeepLException(
                            "Not found, check server_url",
                            http_status_code=response.status
                        )
                    
                    elif response.status == 400:
                        error_info = ""
                        try:
                            error_json = await response.json()
                            error_info = f": {error_json.get('message', content)}"
                        except:
                            error_info = f": {content}"
                        raise DeepLException(
                            f"Bad request{error_info}",
                            http_status_code=response.status
                        )
                    
                    elif response.status == 429:
                        if attempt < self.max_retries:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        raise TooManyRequestsException(
                            "Too many requests, DeepL servers are currently experiencing high load",
                            http_status_code=response.status,
                            should_retry=True
                        )
                    
                    elif response.status == self._HTTP_STATUS_QUOTA_EXCEEDED:
                        raise QuotaExceededException(
                            "Character limit exceeded",
                            http_status_code=response.status
                        )
                    
                    elif response.status >= 500:
                        if attempt < self.max_retries:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        raise DeepLException(
                            f"Server error: {response.status}",
                            http_status_code=response.status,
                            should_retry=True
                        )
                    
                    else:
                        raise DeepLException(
                            f"Unexpected status code: {response.status}, content: {content}",
                            http_status_code=response.status
                        )
            
            except aiohttp.ClientError as e:
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise DeepLException(f"Connection error: {str(e)}")
        
        raise DeepLException("Max retries exceeded")
    
    async def translate_text(
        self,
        text: Union[str, List[str]],
        *,
        target_lang: str,
        source_lang: Optional[str] = None,
        split_sentences: Union[str, SplitSentences] = SplitSentences.ON,
        formality: Union[str, Formality] = Formality.DEFAULT,
        glossary_id: Optional[str] = None,
        context: Optional[str] = None,
        tag_handling: Optional[str] = None,
        outline_detection: Optional[bool] = None,
        splitting_tags: Optional[List[str]] = None,
        non_splitting_tags: Optional[List[str]] = None,
        ignore_tags: Optional[List[str]] = None,
        model_type: Union[str, ModelType] = ModelType.LATENCY_OPTIMIZED,
        show_billed_characters: Optional[bool] = False
    ) -> Union[TextResult, List[TextResult]]:
        """
        Translate text using the DeepL API.
        
        Args:
            text: Text(s) to translate. Can be a string or list of strings.
            target_lang: Target language code (e.g., "DE", "EN-US", "FR").
            source_lang: Source language code. If None, language will be auto-detected.
            split_sentences: How to split sentences. Default: SplitSentences.ON.
            formality: Formality level. Default: Formality.DEFAULT.
            glossary_id: ID of glossary to use for translation.
            context: Additional context to influence translation.
            tag_handling: Type of tags to handle ("xml" or "html").
            outline_detection: Whether to enable outline detection for XML.
            splitting_tags: XML tags that should split sentences.
            non_splitting_tags: XML tags that should never split sentences.
            ignore_tags: XML tags that should not be translated.
            model_type: Translation model to use. Default: ModelType.LATENCY_OPTIMIZED.
            
        Returns:
            TextResult or List[TextResult] depending on input type.
        """
        # Handle input validation
        if isinstance(text, str):
            if not text.strip():
                raise ValueError("text must not be empty")
            text_list = [text]
            single_input = True
        elif hasattr(text, "__iter__"):
            text_list = list(text)
            if not text_list:
                raise ValueError("text list must not be empty")
            single_input = False
        else:
            raise TypeError("text must be a string or iterable of strings")
        
        if not target_lang:
            raise ValueError("target_lang is required")

        if target_lang.lower() not in LANGKEYS and target_lang.lower() not in LANGNAMES:
            raise ValueError(f"Invalid target_lang: {target_lang}. Must be in LANGKEYS or LANGNAMES.")
        
        if target_lang.lower() in LANGNAMES:
            target_lang = LANGCODES.get(target_lang.lower(), target_lang)
        
        # Build request data
        request_data = {
            "text": text_list,
            "target_lang": target_lang.upper()
        }
        
        if source_lang:
            if source_lang.lower() in SOURCE_LANGNAMES:
                source_lang = SOURCE_LANGCODES.get(source_lang.lower(), source_lang)
            if source_lang.lower() in SOURCE_LANGKEYS:
                request_data["source_lang"] = source_lang.lower()
        
        if isinstance(split_sentences, SplitSentences):
            request_data["split_sentences"] = split_sentences.value
        else:
            request_data["split_sentences"] = str(split_sentences)
        
        if isinstance(formality, Formality):
            request_data["formality"] = formality.value
        elif formality != "default":
            request_data["formality"] = formality
        
        if glossary_id:
            request_data["glossary_id"] = glossary_id
        
        if context:
            request_data["context"] = context
        
        if tag_handling:
            request_data["tag_handling"] = tag_handling
        
        if outline_detection is not None:
            request_data["outline_detection"] = "1" if outline_detection else "0"
        
        if splitting_tags:
            request_data["splitting_tags"] = ",".join(splitting_tags)
        
        if non_splitting_tags:
            request_data["non_splitting_tags"] = ",".join(non_splitting_tags)
        
        if ignore_tags:
            request_data["ignore_tags"] = ",".join(ignore_tags)
        
        if isinstance(model_type, ModelType):
            request_data["model_type"] = model_type.value
        else:
            request_data["model_type"] = model_type

        if show_billed_characters:
            request_data["show_billed_characters"] = True

        # Make request
        response = await self._make_request("v2/translate", request_data)
        
        # Parse response
        translations = response.get("translations", [])
        results = []

        for i, translation in enumerate(translations):
            result = TextResult(
                text=translation.get("text", ""),
                input=text[i] if isinstance(text, list) else text,
                src=translation.get("detected_source_language", ""),
                dest=target_lang,
                billed_characters=translation.get("billed_characters"),
                model_type_used=translation.get("model_type_used")
            )
            results.append(result)
        
        return results[0] if single_input else results
    
    async def get_usage(self) -> Usage:
        """Get current API usage information."""
        response = await self._make_request("v2/usage", method="GET")
        return Usage(
            character_count=response.get("character_count", 0),
            character_limit=response.get("character_limit", 0)
        )
    
    async def get_source_languages(self) -> List[Language]:
        """Get list of supported source languages."""
        response = await self._make_request("v2/languages?type=source", method="GET")
        return [
            Language(
                code=lang.get("language", ""),
                name=lang.get("name", ""),
                supports_formality=lang.get("supports_formality", False)
            )
            for lang in response
        ]
    
    async def get_target_languages(self) -> List[Language]:
        """Get list of supported target languages."""
        response = await self._make_request("v2/languages?type=target", method="GET")
        return [
            Language(
                code=lang.get("language", ""),
                name=lang.get("name", ""),
                supports_formality=lang.get("supports_formality", False)
            )
            for lang in response
        ]