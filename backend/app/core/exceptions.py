class DeploymentConfigurationError(Exception):
    """
    Raised when environment or deployment configuration is invalid,
    such as missing Playwright Chromium browser binaries or missing system dependencies.
    """
    def __init__(self, message: str = "Chromium browser is not installed. Run: playwright install chromium"):
        self.message = message
        super().__init__(self.message)
