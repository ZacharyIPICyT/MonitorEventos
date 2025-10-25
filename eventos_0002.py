import cv2
import pandas as pd
import os
from datetime import datetime

class VideoEventMonitor:
    def __init__(self):
        self.events = {
            'acicalamiento': None,
            'exploracion_pared': None,
            'exploracion_arena': None,
            'interaccion_objeto_nuevo': None,
            'interaccion_objeto_control': None
        }
        
        self.event_names_es = {
            'acicalamiento': 'Acicalamiento',
            'exploracion_pared': 'Exploración en pared',
            'exploracion_arena': 'Exploración en arena',
            'interaccion_objeto_nuevo': 'Interacción con objeto nuevo',
            'interaccion_objeto_control': 'Interacción con objeto control'
        }
        
        self.active_events = {}
        self.mouse_id = ""
        self.video_path = ""
        self.output_file = ""
        self.just_activated = False
        self.all_events_data = []  # Para almacenar todos los eventos individuales
        
    def clean_path(self, path):
        """Limpia la ruta quitando comillas y espacios extras"""
        return path.strip().strip('"').strip("'")
        
    def get_video_path(self):
        """Solicita la ruta del video"""
        while True:
            path_input = input("Ingresa la ruta del video: ")
            self.video_path = self.clean_path(path_input)
            
            if os.path.exists(self.video_path):
                print(f"✅ Video encontrado: {os.path.basename(self.video_path)}")
                return True
            else:
                print("❌ Error: El archivo no existe. Intenta nuevamente.")
                print("💡 Sugerencia: Copia la ruta directamente del explorador de archivos")
                print("   Ejemplo: C:\\Users\\admin\\Downloads\\video.mp4")
    
    def get_mouse_id(self):
        """Solicita la ID del ratón"""
        self.mouse_id = input("Ingresa la ID del ratón: ").strip()
    
    def configure_keys(self):
        """Configura las teclas para cada evento"""
        print("\n🎹 CONFIGURACIÓN DE TECLAS PARA EVENTOS")
        print("Presiona la tecla que deseas asignar para cada evento")
        print("Presiona 's' para saltar un evento\n")
        
        for event_key, event_name in self.event_names_es.items():
            while True:
                key_input = input(f"Tecla para '{event_name}' (presiona 's' para saltar): ").strip().lower()
                
                if key_input == 's' or key_input == 'saltar':
                    print(f"✅ Evento '{event_name}' saltado")
                    break
                elif len(key_input) == 1 and key_input.isprintable():
                    if key_input not in self.events.values():
                        self.events[event_key] = key_input
                        print(f"✅ Tecla '{key_input}' asignada a '{event_name}'")
                        break
                    else:
                        print("❌ Esa tecla ya está asignada a otro evento")
                else:
                    print("❌ Por favor ingresa solo un carácter válido")
    
    def setup_output_file(self):
        """Configura el archivo de salida"""
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        self.output_file = f"eventos_{self.mouse_id}_{base_name}.csv"
        
        # Crear DataFrame inicial
        self.df = pd.DataFrame(columns=[
            'mouse_id', 'evento', 'inicio', 'fin', 'duracion', 'evento_numero'
        ])
    
    def show_instructions(self):
        """Muestra las instrucciones en pantalla"""
        instructions = [
            "\n🎯 INSTRUCCIONES:",
            f"Mouse ID: {self.mouse_id}",
            "Video: " + os.path.basename(self.video_path),
            f"Ruta: {self.video_path}",
            "\nTECLAS ASIGNADAS:"
        ]
        
        active_events = 0
        for event_key, event_name in self.event_names_es.items():
            key = self.events[event_key]
            if key:
                instructions.append(f"  {key}: {event_name}")
                active_events += 1
        
        if active_events == 0:
            instructions.append("  ⚠️  No hay eventos configurados")
        
        instructions.extend([
            "\nCONTROLES:",
            "  Espacio: Pausar/Reanudar video",
            "  r: Reiniciar evento actual", 
            "  q: Salir y guardar",
            "  s: Guardar progreso actual",
            "\n📝 COMPORTAMIENTO DE EVENTOS:",
            "  - Presiona una tecla de evento para ACTIVARLO",
            "  - Presiona CUALQUIER OTRA tecla para DESACTIVARLO",
            "  - Los controles (espacio, s, r) no desactivan eventos",
            "  - Solo puede haber UN evento activo a la vez",
            "\nPresiona Enter para comenzar..."
        ])
        
        print("\n".join(instructions))
    
    def monitor_events(self):
        """Monitorea los eventos en el video"""
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print(f"❌ Error: No se pudo abrir el video: {self.video_path}")
            print("💡 Verifica que el archivo no esté corrupto y sea un formato compatible")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"📊 Información del video:")
        print(f"   - FPS: {fps:.2f}")
        print(f"   - Duración: {duration:.2f} segundos")
        print(f"   - Frames: {total_frames}")
        
        paused = False
        current_time = 0
        event_counter = {event_key: 0 for event_key in self.events.keys()}  # Contador por evento
        
        cv2.namedWindow('Monitor de Eventos', cv2.WINDOW_NORMAL)
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            
            # Mostrar información en el frame
            info_frame = frame.copy()
            
            # Información general
            cv2.putText(info_frame, f"Mouse: {self.mouse_id}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(info_frame, f"Tiempo: {current_time:.2f}s / {duration:.2f}s", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(info_frame, f"Frame: {frame_number}/{total_frames}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(info_frame, "PAUSADO" if paused else "REPRODUCIENDO", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if paused else (0, 255, 0), 2)
            
            # Eventos activos
            y_pos = 150
            if self.active_events:
                cv2.putText(info_frame, "EVENTO ACTIVO:", (10, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                y_pos += 30
                
                for event_key, event_data in self.active_events.items():
                    event_name_es = self.event_names_es[event_key]
                    duration_active = current_time - event_data['start_time']
                    cv2.putText(info_frame, f"▶ {event_name_es}: {duration_active:.2f}s", 
                               (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    y_pos += 30
                    
                # Instrucción para desactivar
                cv2.putText(info_frame, "Presiona CUALQUIER OTRA tecla para desactivar", (10, y_pos + 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 100), 1)
            else:
                cv2.putText(info_frame, "No hay eventos activos", (10, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 2)
                y_pos += 40
            
            # Leyenda de teclas
            cv2.putText(info_frame, "TECLAS ASIGNADAS:", (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_pos += 25
            
            for event_key, key in self.events.items():
                if key:
                    event_name_es = self.event_names_es[event_key]
                    # Acortar nombre si es muy largo
                    display_name = event_name_es[:20] + "..." if len(event_name_es) > 20 else event_name_es
                    cv2.putText(info_frame, f"{key}: {display_name}", (10, y_pos), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                    y_pos += 20
            
            # Controles
            controls_y = info_frame.shape[0] - 80
            cv2.putText(info_frame, "CONTROLES: [ESPACIO]Pausa [r]Reiniciar [s]Guardar [q]Salir", 
                       (10, controls_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 255), 1)
            
            cv2.imshow('Monitor de Eventos', info_frame)
            
            key = cv2.waitKey(1 if not paused else 0) & 0xFF
            
            # Si no se presionó tecla, continuar
            if key == 255:
                self.just_activated = False  # Resetear la bandera después de un frame
                continue
            
            # Controles especiales (NO desactivan eventos)
            if key == ord('q'):  # Salir
                break
            elif key == ord(' '):  # Pausar/Reanudar
                paused = not paused
                print("⏸️  Pausado" if paused else "▶️  Reanudado")
                continue
            elif key == ord('s'):  # Guardar progreso
                self.save_progress()
                print("💾 Progreso guardado")
                continue
            elif key == ord('r'):  # Reiniciar evento actual
                self.deactivate_all_events(current_time)
                print("🔄 Eventos activos reiniciados")
                continue
            
            # Lógica de eventos
            event_activated = False
            
            # Primero verificar si es una tecla de evento para ACTIVAR
            for event_key, assigned_key in self.events.items():
                if assigned_key and key == ord(assigned_key):
                    if not self.active_events:  # Solo activar si no hay evento activo
                        event_counter[event_key] += 1  # Incrementar contador
                        self.activate_event(event_key, current_time, event_counter[event_key])
                        event_activated = True
                        self.just_activated = True
                    break
            
            # Si no se activó un evento y hay evento activo, DESACTIVAR
            if not event_activated and self.active_events and not self.just_activated:
                self.deactivate_all_events(current_time)
            
            # Resetear la bandera después de procesar
            self.just_activated = False
        
        # Desactivar cualquier evento activo al final
        self.deactivate_all_events(current_time)
        cap.release()
        cv2.destroyAllWindows()
    
    def activate_event(self, event_key, current_time, event_number):
        """Activa un evento"""
        self.active_events[event_key] = {
            'start_time': current_time, 
            'event_number': event_number
        }
        print(f"▶️  {self.event_names_es[event_key]} #{event_number} INICIADO: {current_time:.2f}s")
        print("   💡 Presiona CUALQUIER OTRA tecla para finalizar")
    
    def deactivate_event(self, event_key, current_time):
        """Desactiva un evento específico"""
        if event_key in self.active_events:
            event_data = self.active_events[event_key]
            duration = current_time - event_data['start_time']
            
            # Guardar datos para el informe
            event_info = {
                'evento': event_key,
                'nombre_es': self.event_names_es[event_key],
                'inicio': event_data['start_time'],
                'fin': current_time,
                'duracion': duration,
                'evento_numero': event_data['event_number']
            }
            self.all_events_data.append(event_info)
            
            # Agregar al DataFrame
            new_row = {
                'mouse_id': self.mouse_id,
                'evento': self.event_names_es[event_key],
                'inicio': event_data['start_time'],
                'fin': current_time,
                'duracion': duration,
                'evento_numero': event_data['event_number']
            }
            
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            del self.active_events[event_key]
            
            print(f"⏹️  {self.event_names_es[event_key]} #{event_data['event_number']} FINALIZADO: "
                  f"{event_data['start_time']:.2f}s - {current_time:.2f}s "
                  f"(duración: {duration:.2f}s)")
    
    def deactivate_all_events(self, current_time):
        """Desactiva todos los eventos activos"""
        for event_key in list(self.active_events.keys()):
            self.deactivate_event(event_key, current_time)
    
    def save_progress(self):
        """Guarda el progreso en el archivo CSV"""
        try:
            self.df.to_csv(self.output_file, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False
    
    def generate_report(self):
        """Genera un informe detallado en formato TXT"""
        if not self.all_events_data:
            print("⚠️  No hay datos para generar el informe")
            return
        
        # Nombre del archivo de informe con el formato solicitado
        fecha_prueba = datetime.now().strftime("%d-%m-%Y")  # Formato: dia-mes-año
        report_file = f"{self.mouse_id}_{fecha_prueba}.txt"
        
        # Calcular estadísticas
        eventos_por_tipo = {}
        duracion_total_por_tipo = {}
        eventos_individuales_por_tipo = {}
        
        for event_data in self.all_events_data:
            event_key = event_data['evento']
            
            if event_key not in eventos_por_tipo:
                eventos_por_tipo[event_key] = 0
                duracion_total_por_tipo[event_key] = 0
                eventos_individuales_por_tipo[event_key] = []
            
            eventos_por_tipo[event_key] += 1
            duracion_total_por_tipo[event_key] += event_data['duracion']
            eventos_individuales_por_tipo[event_key].append(event_data)
        
        # Generar contenido del informe
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("INFORME DE ANÁLISIS DE COMPORTAMIENTO\n")
            f.write("=" * 60 + "\n\n")
            
            # Información general
            f.write("INFORMACIÓN GENERAL\n")
            f.write("-" * 40 + "\n")
            f.write(f"ID del animal: {self.mouse_id}\n")
            f.write(f"Fecha de la prueba: {fecha_actual}\n")
            f.write(f"Video analizado: {os.path.basename(self.video_path)}\n")
            f.write(f"Duración total del video: {self.get_video_duration():.2f} segundos\n\n")
            
            # Resumen de tiempos y frecuencias
            f.write("RESUMEN DE COMPORTAMIENTOS\n")
            f.write("-" * 40 + "\n")
            
            for event_key, event_name in self.event_names_es.items():
                if self.events[event_key]:  # Solo si tiene tecla asignada
                    frecuencia = eventos_por_tipo.get(event_key, 0)
                    tiempo_total = duracion_total_por_tipo.get(event_key, 0)
                    
                    f.write(f"{event_name}:\n")
                    f.write(f"  Tiempo total: {tiempo_total:.2f}s\n")
                    f.write(f"  Frecuencia: {frecuencia} interacciones\n\n")
            
            # Tablas detalladas por evento
            f.write("DETALLE POR EVENTO\n")
            f.write("=" * 60 + "\n\n")
            
            for event_key, event_name in self.event_names_es.items():
                if self.events[event_key] and event_key in eventos_individuales_por_tipo:
                    f.write(f"{event_name.upper()}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"{'Duración':<10} | {'Intervalo del Video':<30} | {'Evento'}\n")
                    f.write("-" * 50 + "\n")
                    
                    for event_data in eventos_individuales_por_tipo[event_key]:
                        duracion_str = f"{event_data['duracion']:.2f}s"
                        intervalo_str = f"{event_data['inicio']:.2f}s - {event_data['fin']:.2f}s"
                        evento_num = event_data['evento_numero']
                        
                        f.write(f"{duracion_str:<10} | {intervalo_str:<30} | {evento_num}\n")
                    
                    f.write("\n")
        
        print(f"📄 Informe generado: {report_file}")
        return report_file
    
    def get_video_duration(self):
        """Obtiene la duración del video"""
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            return 0
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        cap.release()
        
        return duration
    
    def run(self):
        """Ejecuta el programa completo"""
        print("🐭 MONITOR DE EVENTOS EN VIDEO")
        print("=" * 50)
        
        # Configuración inicial
        if not self.get_video_path():
            return
        
        self.get_mouse_id()
        self.configure_keys()
        self.setup_output_file()
        self.show_instructions()
        
        # Esperar para comenzar
        input()
        
        # Monitorear eventos
        print("\n🎬 Iniciando monitoreo...")
        self.monitor_events()
        
        # Guardar resultados finales
        if not self.df.empty:
            if self.save_progress():
                print(f"💾 Resultados guardados en: {self.output_file}")
                print(f"📊 Total de eventos registrados: {len(self.df)}")
                
                # Generar informe
                print("\n📄 Generando informe detallado...")
                report_file = self.generate_report()
                
                print("\n📈 Resumen de eventos:")
                print(self.df.groupby('evento').size())
            else:
                print("❌ Error al guardar los resultados finales")
        else:
            print("⚠️  No se registraron eventos")
        
        print("👋 Programa terminado")

# Ejecutar el programa
if __name__ == "__main__":
    monitor = VideoEventMonitor()
    monitor.run()