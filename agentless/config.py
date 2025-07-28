from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="AGENTLESS", load_dotenv=True)
