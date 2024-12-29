class BaseStringLog:
    def to_str(self):
        raise NotImplementedError()


class BaseDictLog:
    def to_dict(self):
        raise NotImplementedError()


class HTTPLog(BaseDictLog, BaseStringLog):
    def __init__(
            self,
            url: str,
            method: str,
            headers: list[tuple[bytes, bytes]] |
                     list[tuple[str, str]] |
                     dict[str, list[str]] | None
    ):
        if headers is None:
            headers = dict()
        self._headers = dict()
        self.headers = headers
        self.url = url
        self.method = method

    @property
    def headers(self) -> dict[str, list[str]]:
        return self._headers

    @headers.setter
    def headers(
            self,
            headers: list[tuple[bytes, bytes]] |
                     list[tuple[str, str]] |
                     dict[str, list[str]]
    ) -> None:
        if len(headers) == 0:
            return
        if isinstance(headers, dict):
            self._headers = headers
        elif isinstance(headers[0][0], bytes):
            converted_headers: dict[str, list[str]] = dict()
            for header in headers:
                converted_headers[header[0].decode()] = [
                    value.decode() for value in header[1:]
                ]
            self._headers = converted_headers
        elif isinstance(headers[0][0], str):
            converted_headers: dict[str, list[str]] = dict()
            for header in headers:
                converted_headers[header[0]] = [
                    value.decode() for value in header[1:]
                ]
            self._headers = converted_headers

    def to_dict(self) -> dict:
        return {"url": self.url, "method": self.method, "headers": self.headers}

    def to_str(self) -> str:
        headers_str_list = [
            f"{key}: {', '.join(value)}" for key, value in self._headers.items()
        ]
        return (f"URL: {self.url} | "
                f"Method: {self.method} | "
                f"Headers: [{', '.join(headers_str_list)}]")
