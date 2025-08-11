#!/usr/bin/env python3
"""
Brave Cleaner - Enterprise Edition
Script profesional para limpieza completa de Brave Browser con técnicas anti-antivirus.
Versión: 2.0 - Enterprise Grade
Desarrollado por: w0lfs
Email: olivero_canarios@hotmail.com
"""

import os
import shutil
import subprocess
import time
import winreg
import ctypes
import yaml
from pathlib import Path
from typing import List, Tuple, Optional

def load_config():
    """Cargar configuración enterprise desde archivo YAML."""
    try:
        config_path = Path("config/settings.yaml")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            return {"ui": {"wait_for_exit": True}}
    except Exception:
        return {"ui": {"wait_for_exit": True}}

class WindowsEventCleaner:
    """Limpieza enterprise de eventos de Windows con técnicas anti-antivirus."""
    
    def __init__(self):
        self.cleaned_events = 0
        self.failed_events = 0
        
    def is_admin(self) -> bool:
        """Verificar permisos de administrador."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def clean_registry_key(self, key_path: str, key_name: str = None) -> bool:
        """Limpiar clave del registro de forma segura."""
        try:
            if key_name:
                subprocess.run(['reg', 'delete', key_path, '/v', key_name, '/f'], 
                             capture_output=True, timeout=10)
            else:
                subprocess.run(['reg', 'delete', key_path, '/f'], 
                             capture_output=True, timeout=10)
            
            time.sleep(0.1)  # Delay anti-antivirus
            return True
            
        except Exception:
            return False
    
    def clean_user_assist(self) -> int:
        """Limpiar UserAssist - eventos de aplicaciones ejecutadas."""
        print("🔍 Limpiando UserAssist (eventos de aplicaciones)...")
        
        user_assist_paths = [
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{75048700-EF1F-11D0-9888-006097DEACF9}",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}"
        ]
        
        cleaned = 0
        for path in user_assist_paths:
            if self.clean_registry_key(path):
                print(f"✅ UserAssist limpiado: {path.split('\\')[-1]}")
                cleaned += 1
                time.sleep(0.2)
            else:
                self.failed_events += 1
                
        return cleaned
    
    def clean_run_mru(self) -> int:
        """Limpiar RunMRU - comandos ejecutados recientemente."""
        print("🔍 Limpiando RunMRU (comandos ejecutados)...")
        
        run_mru_path = r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
        
        # Limpiar valores individuales primero
        for i in range(26):
            key_name = chr(ord('a') + i)
            if self.clean_registry_key(run_mru_path, key_name):
                time.sleep(0.05)
        
        # Limpiar clave completa
        if self.clean_registry_key(run_mru_path):
            print("✅ RunMRU completamente limpiado")
            return 1
        else:
            self.failed_events += 1
            return 0
    
    def clean_comdlg32(self) -> int:
        """Limpiar ComDlg32 - archivos abiertos/guardados recientemente."""
        print("🔍 Limpiando ComDlg32 (archivos recientes)...")
        
        comdlg32_paths = [
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\FirstFolder"
        ]
        
        cleaned = 0
        for path in comdlg32_paths:
            if self.clean_registry_key(path):
                print(f"✅ ComDlg32 limpiado: {path.split('\\')[-1]}")
                cleaned += 1
                time.sleep(0.2)
            else:
                self.failed_events += 1
                
        return cleaned
    
    def clean_typed_paths(self) -> int:
        """Limpiar TypedPaths - rutas escritas en explorador."""
        print("🔍 Limpiando TypedPaths (rutas del explorador)...")
        
        typed_paths = [
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery"
        ]
        
        cleaned = 0
        for path in typed_paths:
            if self.clean_registry_key(path):
                print(f"✅ TypedPaths limpiado: {path.split('\\')[-1]}")
                cleaned += 1
                time.sleep(0.2)
            else:
                self.failed_events += 1
                
        return cleaned
    
    def clean_windows_search(self) -> int:
        """Limpiar Windows Search - búsquedas recientes."""
        print("🔍 Limpiando Windows Search (búsquedas recientes)...")
        
        search_paths = [
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_TrackDocs"
        ]
        
        cleaned = 0
        for path in search_paths:
            if self.clean_registry_key(path):
                print(f"✅ Windows Search limpiado: {path.split('\\')[-1]}")
                cleaned += 1
                time.sleep(0.2)
            else:
                self.failed_events += 1
                
        return cleaned
    
    def clean_all_windows_events(self) -> Tuple[int, int]:
        """Limpiar TODOS los eventos de Windows de forma segura."""
        print("\n🔥 LIMPIANDO EVENTOS DE WINDOWS (ANTI-ANTIVIRUS)...")
        print("=" * 60)
        
        total_cleaned = 0
        
        total_cleaned += self.clean_user_assist()
        total_cleaned += self.clean_run_mru()
        total_cleaned += self.clean_comdlg32()
        total_cleaned += self.clean_typed_paths()
        total_cleaned += self.clean_windows_search()
        
        print(f"📊 Eventos de Windows: {total_cleaned} limpiados, {self.failed_events} fallidos")
        
        return total_cleaned, self.failed_events

class BraveDataCleaner:
    """Limpieza enterprise de datos de Brave con técnicas anti-antivirus."""
    
    def __init__(self):
        self.deleted_count = 0
        self.total_size_freed = 0
        self.failed_deletions = 0
        
    def close_brave_safely(self) -> bool:
        """Cerrar Brave de forma segura."""
        print("🔍 Cerrando Brave de forma segura...")
        
        try:
            result = subprocess.run(['taskkill', '/im', 'brave.exe'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Brave cerrado exitosamente")
            else:
                print("ℹ️ Brave no estaba ejecutándose")
            
            time.sleep(2)
            
            result = subprocess.run(['tasklist', '/fi', 'imagename eq brave.exe'], 
                                  capture_output=True, text=True)
            
            if 'brave.exe' not in result.stdout:
                print("✅ Todos los procesos de Brave cerrados")
                return True
            else:
                print("⚠️ Algunos procesos de Brave pueden seguir ejecutándose")
                return False
                
        except Exception as e:
            print(f"❌ Error al cerrar Brave: {e}")
            return False
    
    def force_delete_file_safe(self, file_path: Path, max_attempts: int = 3) -> bool:
        """Eliminar archivo de forma segura con múltiples intentos."""
        for attempt in range(max_attempts):
            try:
                if file_path.exists():
                    file_path.chmod(0o777)
                    file_path.unlink()
                    
                    if not file_path.exists():
                        return True
                    
                time.sleep(0.1 * (attempt + 1))
                
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(0.5)
                    continue
                else:
                    return False
            except Exception:
                return False
                
        return False
    
    def force_delete_directory_safe(self, dir_path: Path) -> bool:
        """Eliminar directorio de forma segura."""
        try:
            if dir_path.exists():
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    for file in files:
                        try:
                            file_path = Path(root) / file
                            file_path.chmod(0o777)
                        except:
                            pass
                    for dir in dirs:
                        try:
                            dir_path_full = Path(root) / dir
                            dir_path_full.chmod(0o777)
                        except:
                            pass
                
                dir_path.chmod(0o777)
                shutil.rmtree(dir_path, ignore_errors=True)
                
                return not dir_path.exists()
                
        except Exception:
            return False
    
    def clean_brave_user_data(self) -> Tuple[int, int]:
        """Limpiar datos de usuario de Brave."""
        print("🧹 Limpiando datos de usuario de Brave...")
        
        brave_paths = [
            Path(os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data")),
            Path(os.path.expandvars(r"%APPDATA%\BraveSoftware\Brave-Browser\User Data")),
            Path(os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware")),
            Path(os.path.expandvars(r"%APPDATA%\BraveSoftware"))
        ]
        
        deleted = 0
        size_freed = 0
        
        for brave_path in brave_paths:
            if brave_path.exists():
                print(f"🔍 Limpiando: {brave_path}")
                
                try:
                    size_before = sum(f.stat().st_size for f in brave_path.rglob('*') if f.is_file())
                    
                    if self.force_delete_directory_safe(brave_path):
                        print(f"✅ Eliminado: {brave_path.name}")
                        deleted += 1
                        size_freed += size_before
                    else:
                        print(f"⚠️ No se pudo eliminar completamente: {brave_path.name}")
                        self.failed_deletions += 1
                        
                except Exception as e:
                    print(f"❌ Error al eliminar {brave_path.name}: {e}")
                    self.failed_deletions += 1
            else:
                print(f"ℹ️ No existe: {brave_path}")
                
        return deleted, size_freed
    
    def clean_system_cache(self) -> Tuple[int, int]:
        """Limpiar caché del sistema de forma segura."""
        print("🧹 Limpiando caché del sistema...")
        
        cache_paths = [
            Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\INetCache")),
            Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\WebCache")),
            Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Cookies")),
            Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\History"))
        ]
        
        deleted = 0
        size_freed = 0
        
        for cache_path in cache_paths:
            if cache_path.exists():
                print(f"🔍 Limpiando caché: {cache_path.name}")
                
                try:
                    size_before = sum(f.stat().st_size for f in cache_path.rglob('*') if f.is_file())
                    
                    if self.force_delete_directory_safe(cache_path):
                        print(f"✅ Caché eliminado: {cache_path.name}")
                        deleted += 1
                        size_freed += size_before
                    else:
                        print(f"⚠️ No se pudo eliminar caché: {cache_path.name}")
                        self.failed_deletions += 1
                        
                except Exception as e:
                    print(f"❌ Error al eliminar caché {cache_path.name}: {e}")
                    self.failed_deletions += 1
            else:
                print(f"ℹ️ No existe caché: {cache_path}")
                
        return deleted, size_freed
    
    def clean_temp_files(self) -> Tuple[int, int]:
        """Limpiar archivos temporales de forma segura."""
        print("🧹 Limpiando archivos temporales...")
        
        temp_paths = [
            Path(os.path.expandvars(r"%TEMP%")),
            Path(os.path.expandvars(r"%LOCALAPPDATA%\Temp")),
            Path(os.path.expandvars(r"%WINDIR%\Temp"))
        ]
        
        brave_patterns = [
            "*brave*", "*Brave*", "*BRAVE*", "*.brave*",
            "*brave-browser*", "*brave_*", "*_brave*",
            "*chrome*", "*Chrome*", "*CHROME*"
        ]
        
        deleted = 0
        size_freed = 0
        
        for temp_path in temp_paths:
            if temp_path.exists():
                print(f"🔍 Buscando archivos temporales en: {temp_path.name}")
                
                for pattern in brave_patterns:
                    try:
                        for file_path in temp_path.glob(pattern):
                            if file_path.is_file():
                                try:
                                    file_size = file_path.stat().st_size
                                    if self.force_delete_file_safe(file_path):
                                        print(f"🗑️ Archivo temporal eliminado: {file_path.name}")
                                        deleted += 1
                                        size_freed += file_size
                                    else:
                                        self.failed_deletions += 1
                                except Exception:
                                    self.failed_deletions += 1
                        
                        for dir_path in temp_path.glob(pattern):
                            if dir_path.is_dir():
                                try:
                                    dir_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                                    if self.force_delete_directory_safe(dir_path):
                                        print(f"🗑️ Directorio temporal eliminado: {dir_path.name}")
                                        deleted += 1
                                        size_freed += dir_size
                                    else:
                                        self.failed_deletions += 1
                                except Exception:
                                    self.failed_deletions += 1
                                    
                    except Exception as e:
                        print(f"❌ Error buscando patrón {pattern}: {e}")
                        
        return deleted, size_freed

def clean_brave_completely():
    """Función principal de limpieza enterprise."""
    print("🔥 ELIMINACIÓN ENTERPRISE COMPLETA DE BRAVE")
    print("=" * 60)
    
    event_cleaner = WindowsEventCleaner()
    data_cleaner = BraveDataCleaner()
    
    total_deleted = 0
    total_size_freed = 0
    
    data_cleaner.close_brave_safely()
    
    print("\n🔥 LIMPIANDO DATOS DE BRAVE...")
    deleted, size_freed = data_cleaner.clean_brave_user_data()
    total_deleted += deleted
    total_size_freed += size_freed
    
    print("\n🔥 LIMPIANDO CACHÉ DEL SISTEMA...")
    deleted, size_freed = data_cleaner.clean_system_cache()
    total_deleted += deleted
    total_size_freed += size_freed
    
    print("\n🔥 LIMPIANDO ARCHIVOS TEMPORALES...")
    deleted, size_freed = data_cleaner.clean_temp_files()
    total_deleted += deleted
    total_size_freed += size_freed
    
    events_cleaned, events_failed = event_cleaner.clean_all_windows_events()
    
    print("\n" + "=" * 60)
    print("🎯 ELIMINACIÓN ENTERPRISE COMPLETA FINALIZADA")
    print(f"📊 Elementos eliminados: {total_deleted}")
    print(f"💾 Espacio liberado: {total_size_freed / (1024*1024):.2f} MB")
    print(f"🔍 Eventos de Windows limpiados: {events_cleaned}")
    print(f"⚠️ Fallos totales: {data_cleaner.failed_deletions + events_failed}")
    print("=" * 60)
    
    return total_deleted > 0 or events_cleaned > 0

def main():
    """Función principal enterprise."""
    config = load_config()
    
    print("🚀 BRAVE CLEANER - ENTERPRISE EDITION 2.0")
    print("⚠️  ADVERTENCIA: Esto eliminará TODOS los datos de Brave")
    print("⚠️  Incluyendo eventos de Windows y datos del sistema")
    print("=" * 60)
    
    if not WindowsEventCleaner().is_admin():
        print("⚠️  RECOMENDACIÓN: Ejecutar como administrador para limpieza completa")
        print("⚠️  Algunos eventos de Windows pueden no limpiarse completamente")
    
    confirm = input("¿Está seguro de que desea continuar? (sí/no): ").lower()
    if confirm not in ['sí', 'si', 'yes', 'y', 's']:
        print("❌ Operación cancelada por el usuario")
        return
    
    if clean_brave_completely():
        print("\n🎉 ¡ELIMINACIÓN ENTERPRISE COMPLETA EXITOSA!")
        print("💡 Todos los datos de Brave han sido eliminados del sistema")
        print("💡 Incluyendo eventos de Windows y datos de la base de datos local")
        print("💡 Sistema completamente limpio y optimizado")
    else:
        print("\n❌ La eliminación completa falló")
    
    if config.get("ui", {}).get("wait_for_exit", True):
        print("\n" + "=" * 60)
        input("Presione Enter para cerrar el programa...")

if __name__ == "__main__":
    main() 