"""
PyQt6 Main Application Window
InstaVideo Studio Desktop Client
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QTabWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        self.setWindowTitle(f"{settings.APP_NAME} v{settings.APP_VERSION}")
        self.setWindowIcon(self._create_icon())
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize UI
        self._init_ui()
        
        # Apply theme
        self._apply_theme()
    
    def _init_ui(self):
        """Initialize user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Sidebar
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Tab widget for main content
        tabs = QTabWidget()
        tabs.addTab(self._create_dashboard_tab(), "Dashboard")
        tabs.addTab(self._create_downloads_tab(), "Downloads")
        tabs.addTab(self._create_library_tab(), "Biblioteca")
        tabs.addTab(self._create_editor_tab(), "Editor")
        tabs.addTab(self._create_exports_tab(), "Exportações")
        tabs.addTab(self._create_settings_tab(), "Configurações")
        
        main_layout.addWidget(tabs, 1)
    
    def _create_sidebar(self) -> QWidget:
        """Create sidebar widget"""
        sidebar = QWidget()
        sidebar.setMaximumWidth(200)
        layout = QVBoxLayout(sidebar)
        
        # Logo/Title
        title = QLabel(settings.APP_NAME)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Menu buttons
        for button_text in ["Dashboard", "Downloads", "Biblioteca", "Editor", "Exportações", "Configurações"]:
            btn = QPushButton(button_text)
            btn.setMinimumHeight(40)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Footer info
        footer = QLabel("v1.0.0")
        footer.setFont(QFont("Arial", 9))
        layout.addWidget(footer)
        
        return sidebar
    
    def _create_dashboard_tab(self) -> QWidget:
        """Create dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("📊 Dashboard"))
        layout.addWidget(QLabel("Total de vídeos: 0"))
        layout.addWidget(QLabel("Espaço utilizado: 0 MB"))
        layout.addStretch()
        return widget
    
    def _create_downloads_tab(self) -> QWidget:
        """Create downloads tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("⬇️ Gerenciador de Downloads"))
        layout.addWidget(QPushButton("+ Novo Download"))
        layout.addStretch()
        return widget
    
    def _create_library_tab(self) -> QWidget:
        """Create library tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("📹 Biblioteca de Vídeos"))
        layout.addStretch()
        return widget
    
    def _create_editor_tab(self) -> QWidget:
        """Create editor tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("✂️ Editor de Vídeo"))
        layout.addStretch()
        return widget
    
    def _create_exports_tab(self) -> QWidget:
        """Create exports tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("📤 Fila de Exportação"))
        layout.addStretch()
        return widget
    
    def _create_settings_tab(self) -> QWidget:
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("⚙️ Configurações"))
        layout.addStretch()
        return widget
    
    def _apply_theme(self):
        """Apply application theme (dark mode)"""
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QWidget { background-color: #1e1e1e; color: #e0e0e0; }
            QTabWidget::pane { border: 1px solid #3d3d3d; }
            QTabBar::tab { background-color: #2d2d2d; color: #e0e0e0; padding: 5px 15px; }
            QTabBar::tab:selected { background-color: #0078d4; }
            QPushButton { 
                background-color: #0078d4; 
                color: white; 
                border: none; 
                border-radius: 4px; 
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0066b3; }
            QPushButton:pressed { background-color: #004a7f; }
        """)
    
    @staticmethod
    def _create_icon() -> QIcon:
        """Create application icon"""
        # Placeholder - replace with actual icon
        return QIcon()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName(settings.APP_NAME)
    app.setApplicationVersion(settings.APP_VERSION)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
