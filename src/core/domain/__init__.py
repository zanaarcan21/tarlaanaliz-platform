# PATH: src/core/domain/__init__.py
# DESC: Python paket başlangıcı; modül dışa aktarım (exports) ve namespace düzeni.
"""
Domain Core package.

Domain katmanı; entity, value object, service ve event tanımlarını içerir.
Dış dünya erişimi (IO, veritabanı, HTTP) bu katmanda YOKTUR.
Alt modüller: entities, value_objects, services, events.
"""

__all__: list[str] = []
