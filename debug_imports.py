import livekit.plugins
print(f"livekit.plugins path: {livekit.plugins.__path__}")
try:
    from livekit.plugins import noise_cancellation
    print("Successfully imported noise_cancellation")
except ImportError as e:
    print(f"Failed to import noise_cancellation: {e}")

try:
    import livekit.plugins.noise_cancellation
    print("Successfully imported livekit.plugins.noise_cancellation")
except ImportError as e:
    print(f"Failed to import livekit.plugins.noise_cancellation: {e}")

import pkgutil
print("Available plugins:")
for importer, modname, ispkg in pkgutil.iter_modules(livekit.plugins.__path__):
    print(f" - {modname}")
