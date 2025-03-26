# utils/error_handler.py
"""
Centralized error handling for the Indo-Pacific Dashboard.
This utility provides standardized error handling and logging throughout the application.
"""

import logging
import traceback
import sys
import os
import datetime
import streamlit as st

# Configure logger
logger = logging.getLogger("indo_pacific_dashboard")

class DashboardErrorHandler:
    """
    Error handler for the Indo-Pacific Dashboard.
    Provides centralized error handling, logging, and user feedback.
    """
    
    @staticmethod
    def log_error(error, context="", level="error"):
        """
        Log an error with context information.
        
        Parameters:
        -----------
        error : Exception
            The exception to log
        context : str
            Context information about where the error occurred
        level : str
            Log level ('error', 'warning', 'info')
        """
        # Get traceback info
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        # Format message
        message = f"{context} - {str(error)}\n{tb_str}"
        
        # Log at appropriate level
        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        else:
            logger.info(message)
    
    @staticmethod
    def handle_feed_error(error, source_name):
        """
        Handle errors related to feed fetching.
        
        Parameters:
        -----------
        error : Exception
            The exception that occurred
        source_name : str
            Name of the feed source
        """
        # Log the error
        DashboardErrorHandler.log_error(
            error, 
            context=f"Error fetching feed from {source_name}", 
            level="error"
        )
    
    @staticmethod
    def handle_article_error(error, article_data=None):
        """
        Handle errors related to article processing.
        
        Parameters:
        -----------
        error : Exception
            The exception that occurred
        article_data : dict
            Optional article data for context
        """
        # Get article title if available
        article_title = article_data.get('title', 'Unknown article') if article_data else 'Unknown article'
        
        # Log the error
        DashboardErrorHandler.log_error(
            error, 
            context=f"Error processing article: {article_title}", 
            level="warning"
        )
    
    @staticmethod
    def handle_ui_error(error, component="UI"):
        """
        Handle errors related to UI rendering.
        
        Parameters:
        -----------
        error : Exception
            The exception that occurred
        component : str
            Name of the UI component
        """
        # Log the error
        DashboardErrorHandler.log_error(
            error, 
            context=f"Error in UI component: {component}", 
            level="error"
        )
        
        # Show user-friendly error message
        try:
            st.error(f"Error rendering {component}. Please check the logs or try refreshing.")
        except:
            # Can't show streamlit error - already in an error state
            pass
    
    @staticmethod
    def handle_critical_error(error, context=""):
        """
        Handle critical errors that should terminate the application.
        
        Parameters:
        -----------
        error : Exception
            The exception that occurred
        context : str
            Context information
        """
        # Log the critical error
        DashboardErrorHandler.log_error(
            error, 
            context=f"CRITICAL ERROR: {context}", 
            level="error"
        )
        
        # Write to a dedicated error file
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(script_dir, "logs")
            os.makedirs(log_dir, exist_ok=True)
            
            error_file = os.path.join(log_dir, f"critical_error_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"Critical error occurred at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Context: {context}\n")
                f.write(f"Error: {str(error)}\n")
                f.write("Traceback:\n")
                f.write(traceback.format_exc())
        except Exception as write_error:
            # Can't even write to error file
            logger.error(f"Failed to write critical error to file: {str(write_error)}")
        
        # Show fatal error to user
        try:
            st.error("A critical error has occurred. The application may not function correctly.")
            st.info("Please check the logs for details and try restarting the application.")
            
            # Show technical details in expander
            with st.expander("Technical Error Details"):
                st.code(f"Error: {str(error)}\n\n{traceback.format_exc()}", language="python")
        except:
            # Can't show streamlit error - already in an error state
            pass
    
    @staticmethod
    def is_safe_to_continue(error):
        """
        Determine if it's safe to continue execution after an error.
        
        Parameters:
        -----------
        error : Exception
            The exception to evaluate
        
        Returns:
        --------
        bool
            True if it's safe to continue, False if the application should stop
        """
        # List of error types that indicate it's not safe to continue
        critical_error_types = [
            ImportError,      # Missing module
            ModuleNotFoundError,  # Missing module
            OSError,          # File/system errors
            PermissionError,  # Permission issues
            SystemError       # Interpreter error
        ]
        
        # Check if error is a critical type
        for error_type in critical_error_types:
            if isinstance(error, error_type):
                return False
        
        # Check error message for critical keywords
        critical_keywords = [
            "permission denied",
            "access violation",
            "cannot import",
            "no module named",
            "file not found",
            "directory not found"
        ]
        
        error_msg = str(error).lower()
        for keyword in critical_keywords:
            if keyword in error_msg:
                return False
        
        # Default to allowing continuation
        return True
    
    @staticmethod
    def handle_exception(func):
        """
        Decorator to handle exceptions in functions.
        
        Parameters:
        -----------
        func : function
            The function to wrap with error handling
        
        Returns:
        --------
        function
            Wrapped function with error handling
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the error
                DashboardErrorHandler.log_error(
                    e, 
                    context=f"Exception in {func.__name__}", 
                    level="error"
                )
                
                # Check if safe to continue
                if not DashboardErrorHandler.is_safe_to_continue(e):
                    DashboardErrorHandler.handle_critical_error(
                        e, 
                        context=f"Fatal error in {func.__name__}"
                    )
                    # Re-raise to halt execution
                    raise
                
                # Show error to user
                try:
                    st.error(f"An error occurred in {func.__name__}. See logs for details.")
                except:
                    # Can't show streamlit error - already in an error state
                    pass
                
                # Return None or appropriate fallback value
                return None
        
        return wrapper


# Helper functions for common error scenarios
def handle_feed_error(source_name, error):
    """Wrapper for handling feed errors"""
    DashboardErrorHandler.handle_feed_error(error, source_name)
    # Return empty feed data
    return {'entries': [], 'status': 0}

def handle_article_processing_error(article, error):
    """Wrapper for handling article processing errors"""
    DashboardErrorHandler.handle_article_error(error, article)
    # Return basic article data
    return {
        'title': article.get('title', 'Error processing article'),
        'link': article.get('link', ''),
        'date': article.get('date', datetime.datetime.now()),
        'summary': "An error occurred while processing this article.",
        'importance': 1,
        'sentiment': {},
        'categories': {'Error': 1}
    }
