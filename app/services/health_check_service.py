class HealthCheck:
    def check(self):
        """
        Retorna sempre que a API está saudável.
        """
        return {
            "healthy": True,
            "services": {
                "api": True
            }
        }
