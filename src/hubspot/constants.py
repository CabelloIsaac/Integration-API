from .config import Config


class EstadoClickup:
    NO_APTO: str = "No Apto"
    LISTO: str = "Listo"
    EN_SINCRONIZACION: str = "En Sincronización"
    ANADIDO_A_CLICKUP: str = "Añadido a ClickUp"


class Associations:
    DEALS: str = "deals"
    COMPANIES: str = "companies"
    CONTACTS: str = "contacts"
    QUOTES: str = "quotes"
    LINE_ITEMS: str = "line_items"
    CONTRACTS: str = Config.HUBSPOT_CONTRACT_OBJECT_TYPE
    PROJECTS: str = Config.HUBSPOT_PROJECT_OBJECT_TYPE

    
