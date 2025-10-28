import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from eventos_0002 import VideoEventMonitor
    
    def main():
        """Punto de entrada principal de la aplicación"""
        monitor = VideoEventMonitor()
        monitor.run()

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("📁 Archivos en el directorio:")
    for file in os.listdir('.'):
        if file.endswith('.py'):
            print(f"   - {file}")
    input("Presiona Enter para salir...")
