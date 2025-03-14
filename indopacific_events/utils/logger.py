# utils/logger.py
"""
Logging utility for the Indo-Pacific Dashboard.
Provides centralized logging configuration and log viewing functionality.
"""

import logging
import os
import streamlit as st
from datetime import datetime

class DashboardLogger:
    """
    Logger for the Indo-Pacific Dashboard.
    Handles log file creation, log rotation, and provides a UI component for viewing logs.
    """
    
    def __init__(self, script_dir):
        """
        Initialize the logger with the given script directory.
        
        Args:
            script_dir (str): Path to the script directory
        """
        self.script_dir = script_dir
        self.log_dir = os.path.join(script_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.log_dir, f"dashboard_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # Configure the root logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()  # Also output to console for debugging
            ]
        )
        
        # Get a logger for this module
        self.logger = logging.getLogger("indo_pacific_dashboard")
    
    def get_logger(self):
        """Return the configured logger instance."""
        return self.logger
    
    def log_feed_error(self, source_name, error):
        """
        Log an error when fetching a feed.
        
        Args:
            source_name (str): Name of the feed source
            error (Exception): The exception that occurred
        """
        self.logger.error(f"Error fetching feed from {source_name}: {str(error)}")
    
    def log_article_error(self, source_name, error):
        """
        Log an error when processing an article.
        
        Args:
            source_name (str): Name of the feed source
            error (Exception): The exception that occurred
        """
        self.logger.warning(f"Error processing article from {source_name}: {str(error)}")
    
    def create_log_viewer(self):
        """
        Create a Streamlit component to view and manage logs.
        Should be called within a Streamlit app context.
        """
        with st.expander("View Error Logs"):
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    log_content = f.readlines()
                    
                # Filter to show only warnings and errors
                error_logs = [line for line in log_content if 'ERROR' in line or 'WARNING' in line]
                
                # Show the most recent logs (limited to 50 for performance)
                recent_logs = error_logs[-50:] if len(error_logs) > 50 else error_logs
                
                # Display error logs with formatting
                st.text_area("Recent Errors and Warnings", value="".join(recent_logs), height=300)
                
                # Add log management options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Clear Logs"):
                        try:
                            # Backup the log file before clearing
                            backup_file = os.path.join(
                                self.log_dir, 
                                f"dashboard_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_backup.log"
                            )
                            with open(self.log_file, 'r') as src, open(backup_file, 'w') as dst:
                                dst.write(src.read())
                            
                            # Clear the log file
                            with open(self.log_file, 'w') as f:
                                f.write(f"Log cleared at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            
                            st.success("Logs cleared successfully")
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Error clearing logs: {str(e)}")
                
                with col2:
                    if st.button("Download Logs"):
                        try:
                            with open(self.log_file, 'r') as f:
                                log_content = f.read()
                            
                            st.download_button(
                                label="Download Log File",
                                data=log_content,
                                file_name=f"dashboard_logs_{datetime.now().strftime('%Y-%m-%d')}.log",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"Error preparing logs for download: {str(e)}")
            else:
                st.info("No log file found for today.")

# Singleton pattern for the logger
_logger_instance = None

def get_dashboard_logger(script_dir=None):
    """
    Get or create the dashboard logger instance.
    
    Args:
        script_dir (str, optional): Path to the script directory. 
                                    Required only on first call.
    
    Returns:
        DashboardLogger: The dashboard logger instance
    """
    global _logger_instance
    if _logger_instance is None:
        if script_dir is None:
            raise ValueError("script_dir is required for logger initialization")
        _logger_instance = DashboardLogger(script_dir)
    return _logger_instance
