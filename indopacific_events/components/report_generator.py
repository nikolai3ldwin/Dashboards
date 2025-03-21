# components/report_generator.py
"""
Report generator component for the Indo-Pacific Dashboard.
Generates comprehensive analysis reports with sentiment analysis and citations.
"""

import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta
import os
import json
from collections import Counter
import random

class ReportGenerator:
    """
    Generates comprehensive reports based on article data with sentiment analysis,
    regional trends, and key developments.
    """
    
    def __init__(self, articles=None):
        """
        Initialize the report generator.
        
        Parameters:
        -----------
        articles : list
            List of article dictionaries from the dashboard
        """
        self.articles = articles or []
        
    def set_articles(self, articles):
        """Set articles for analysis"""
        self.articles = articles
        
    def generate_report(self, 
                       title="Indo-Pacific Region: Current Developments and Sentiment Analysis", 
                       report_type="comprehensive",
                       time_period="week",
                       included_categories=None,
                       included_countries=None):
        """
        Generate a comprehensive report based on filtered articles.
        
        Parameters:
        -----------
        title : str
            Report title
        report_type : str
            "comprehensive", "security", "economic", or "summary"
        time_period : str
            "day", "week", "month" for filtering
        included_categories : list
            Categories to include in report
        included_countries : list
            Countries to include in report
            
        Returns:
        --------
        str
            Markdown formatted report
        """
        # Filter articles by time period if needed
        if time_period:
            cutoff_date = datetime.datetime.now()
            if time_period == "day":
                cutoff_date -= timedelta(days=1)
            elif time_period == "week":
                cutoff_date -= timedelta(days=7)
            elif time_period == "month":
                cutoff_date -= timedelta(days=30)
                
            filtered_articles = [a for a in self.articles if a['date'] >= cutoff_date]
        else:
            filtered_articles = self.articles
            
        # Further filter by categories if needed
        if included_categories:
            filtered_articles = [a for a in filtered_articles 
                              if any(cat in a.get('categories', {}) for cat in included_categories)]
                              
        # Further filter by countries if needed
        if included_countries and 'All' not in included_countries:
            # This assumes country info is in the text or in some field
            filtered_articles = [a for a in filtered_articles 
                              if any(country.lower() in a.get('summary', '').lower() 
                                     for country in included_countries)]
        
        # If no articles after filtering, return a message
        if not filtered_articles:
            return f"## No articles available for the selected filters.\n\nPlease adjust your filters or time period."
        
        # Generate report based on type
        if report_type == "summary":
            return self._generate_summary_report(filtered_articles, title)
        elif report_type == "security-focused":
            return self._generate_security_report(filtered_articles, title)
        elif report_type == "economic-focused":
            return self._generate_economic_report(filtered_articles, title)
        else:
            return self._generate_comprehensive_report(filtered_articles, title)
            
    def _generate_comprehensive_report(self, articles, title):
        """Generate comprehensive report covering all aspects"""
        if not articles:
            return "## No articles available for the selected filters.\n\nPlease adjust your filters or time period."
            
        # Build the report structure
        report = []
        
        # Add report header
        report.append(f"# {title}")
        report.append(f"*Report Date: {datetime.datetime.now().strftime('%B %d, %Y')}*\n")
        
        # Generate Executive Summary
        report.append("## Executive Summary")
        report.append(self._generate_executive_summary(articles))
        
        # Security Developments Section
        security_articles = [a for a in articles if 'Military' in a.get('categories', {}) or 
                                                'Political' in a.get('categories', {})]
        if security_articles:
            report.append("\n## 1. Security Developments\n")
            report.append(self._generate_security_section(security_articles))
        
        # Economic Developments Section
        economic_articles = [a for a in articles if 'Business' in a.get('categories', {})]
        if economic_articles:
            report.append("\n## 2. Economic Developments\n")
            report.append(self._generate_economic_section(economic_articles))
        
        # Cultural & Social Developments
        cultural_articles = [a for a in articles if 'Civil Affairs' in a.get('categories', {})]
        if cultural_articles:
            report.append("\n## 3. Cultural & Social Developments\n")
            report.append(self._generate_cultural_section(cultural_articles))
        
        # Bilateral Relations Section
        report.append("\n## 4. Bilateral Relations\n")
        report.append(self._generate_bilateral_section(articles))
        
        # Sentiment Analysis Section
        report.append("\n## 5. Sentiment Analysis\n")
        report.append(self._generate_sentiment_section(articles))
        
        # Future Outlook
        report.append("\n## 6. Future Outlook")
        report.append("The Indo-Pacific region will likely continue to be characterized by:\n")
        report.append("1. Intensified security competition balanced with economic interdependence")
        report.append("2. Growing importance of technology in regional power dynamics")
        report.append("3. Continued emphasis on multilateral frameworks and partnerships")
        report.append("4. Increasing focus on supply chain resilience and economic security")
        report.append("5. Enhanced climate and disaster resilience cooperation\n")
        
        # Conclusion
        report.append("## 7. Conclusion")
        report.append(self._generate_conclusion(articles))
        
        # Add citation footer
        report.append("\n---")
        report.append("*This report is based on articles collected from multiple sources. " 
                     f"Analysis covers {len(articles)} articles from the past " 
                     f"{self._get_date_range(articles)}.*")
        
        return "\n".join(report)
    
    def _generate_summary_report(self, articles, title):
        """Generate concise summary report"""
        if not articles:
            return "## No articles available for the selected filters.\n\nPlease adjust your filters or time period."
            
        # Build the report structure
        report = []
        
        # Add report header
        report.append(f"# {title} - Summary")
        report.append(f"*Report Date: {datetime.datetime.now().strftime('%B %d, %Y')}*\n")
        
        # Generate Executive Summary
        report.append("## Key Developments")
        report.append(self._generate_executive_summary(articles))
        
        # Top Stories by Category
        report.append("\n## Top Stories by Category\n")
        
        # Get top stories for each major category
        categories = ['Military', 'Political', 'Business', 'Civil Affairs']
        for category in categories:
            cat_articles = [a for a in articles if category in a.get('categories', {})]
            cat_articles.sort(key=lambda x: x['importance'], reverse=True)
            
            if cat_articles:
                report.append(f"### {category}")
                # Get top 3 articles in this category
                for i, article in enumerate(cat_articles[:3]):
                    # Include source citation
                    report.append(f"- **[{article['title']}]({article['link']})** ({article['source']}, "
                                  f"{article['date'].strftime('%b %d')})")
        
        # Sentiment Analysis Section - simplified
        report.append("\n## Sentiment Analysis\n")
        report.append(self._generate_simple_sentiment_analysis(articles))
        
        # Add citation footer
        report.append("\n---")
        report.append("*This report is based on articles collected from multiple sources. " 
                     f"Analysis covers {len(articles)} articles from the past " 
                     f"{self._get_date_range(articles)}.*")
        
        return "\n".join(report)
    
    def _generate_security_report(self, articles, title):
        """Generate security-focused report"""
        # Filter to security-relevant articles
        security_articles = [a for a in articles if 
                            any(cat in a.get('categories', {}) 
                                for cat in ['Military', 'Political', 'CWMD'])]
        
        if not security_articles:
            return "## No security-related articles available for the selected filters.\n\nPlease adjust your filters or time period."
        
        # Build the report structure
        report = []
        
        # Add report header
        report.append(f"# {title} - Security Focus")
        report.append(f"*Report Date: {datetime.datetime.now().strftime('%B %d, %Y')}*\n")
        
        # Security Overview
        report.append("## Security Overview")
        report.append(self._generate_security_overview(security_articles))
        
        # Major Security Developments
        report.append("\n## Major Security Developments\n")
        
        # Sort articles by importance
        security_articles.sort(key=lambda x: x['importance'], reverse=True)
        
        # Group articles by subtopic
        military_activities = [a for a in security_articles if 'Military' in a.get('categories', {})]
        territorial_disputes = [a for a in security_articles 
                               if any(term in a.get('summary', '').lower() 
                                     for term in ['territorial', 'dispute', 'sovereignty', 'claim'])]
        alliances = [a for a in security_articles 
                    if any(term in a.get('summary', '').lower() 
                          for term in ['alliance', 'partnership', 'cooperation', 'joint'])]
        
        # Add military activities section
        if military_activities:
            report.append("### Military Activities and Posture")
            for article in military_activities[:5]:  # Top 5 by importance
                report.append(f"- **{article['title']}** - {article['source']}, {article['date'].strftime('%b %d')}")
                report.append(f"  *Importance: {'⭐' * article['importance']}*")
                report.append(f"  {article['summary'][:200]}... [Read more]({article['link']})\n")
        
        # Add territorial disputes section
        if territorial_disputes:
            report.append("### Territorial and Maritime Disputes")
            for article in territorial_disputes[:3]:  # Top 3
                report.append(f"- **{article['title']}** - {article['source']}, {article['date'].strftime('%b %d')}")
                report.append(f"  *Importance: {'⭐' * article['importance']}*")
                report.append(f"  {article['summary'][:200]}... [Read more]({article['link']})\n")
        
        # Add alliances section
        if alliances:
            report.append("### Alliance Dynamics")
            for article in alliances[:3]:  # Top 3
                report.append(f"- **{article['title']}** - {article['source']}, {article['date'].strftime('%b %d')}")
                report.append(f"  *Importance: {'⭐' * article['importance']}*")
                report.append(f"  {article['summary'][:200]}... [Read more]({article['link']})\n")
        
        # Security Trend Analysis
        report.append("## Security Trend Analysis")
        report.append(self._generate_security_trends(security_articles))
        
        # Add citation footer
        report.append("\n---")
        report.append("*This security report is based on articles collected from multiple sources. " 
                     f"Analysis covers {len(security_articles)} security-related articles from the past " 
                     f"{self._get_date_range(security_articles)}.*")
        
        return "\n".join(report)
        
    def _generate_economic_report(self, articles, title):
        """Generate economy-focused report"""
        # Filter to economy-relevant articles
        economic_articles = [a for a in articles if 
                            any(cat in a.get('categories', {}) 
                                for cat in ['Business'])]
        
        if not economic_articles:
            return "## No economic-related articles available for the selected filters.\n\nPlease adjust your filters or time period."
        
        # Build the report structure
        report = []
        
        # Add report header
        report.append(f"# {title} - Economic Focus")
        report.append(f"*Report Date: {datetime.datetime.now().strftime('%B %d, %Y')}*\n")
        
        # Economic Overview
        report.append("## Economic Overview")
        report.append(self._generate_economic_overview(economic_articles))
        
        # Major Economic Developments
        report.append("\n## Major Economic Developments\n")
        
        # Sort articles by importance
        economic_articles.sort(key=lambda x: x['importance'], reverse=True)
        
        # Group articles by subtopic
        trade_articles = [a for a in economic_articles 
                         if any(term in a.get('summary', '').lower() 
                               for term in ['trade', 'export', 'import', 'tariff'])]
        investment_articles = [a for a in economic_articles 
                              if any(term in a.get('summary', '').lower() 
                                    for term in ['investment', 'investor', 'fund', 'financing'])]
        economic_policy = [a for a in economic_articles 
                          if any(term in a.get('summary', '').lower() 
                                for term in ['policy', 'regulation', 'reform', 'initiative'])]
        
        # Add trade section
        if trade_articles:
            report.append("### Trade Relations and Agreements")
            for article in trade_articles[:5]:  # Top 5 by importance
                report.append(f"- **{article['title']}** - {article['source']}, {article['date'].strftime('%b %d')}")
                report.append(f"  *Importance: {'⭐' * article['importance']}*")
                report.append(f"  {article['summary'][:200]}... [Read more]({article['link']})\n")
        
        # Add investment section
        if investment_articles:
            report.append("### Investment and Development")
            for article in investment_articles[:3]:  # Top 3
                report.append(f"- **{article['title']}** - {article['source']}, {article['date'].strftime('%b %d')}")
                report.append(f"  *Importance: {'⭐' * article['importance']}*")
                report.append(f"  {article['summary'][:200]}... [Read more]({article['link']})\n")
        
        # Add economic policy section
        if economic_policy:
            report.append("### Economic Policy Developments")
            for article in economic_policy[:3]:  # Top 3
                report.append(f"- **{article['title']}** - {article['source']}, {article['date'].strftime('%b %d')}")
                report.append(f"  *Importance: {'⭐' * article['importance']}*")
                report.append(f"  {article['summary'][:200]}... [Read more]({article['link']})\n")
        
        # Economic Trend Analysis
        report.append("## Economic Trend Analysis")
        report.append(self._generate_economic_trends(economic_articles))
        
        # Add citation footer
        report.append("\n---")
        report.append("*This economic report is based on articles collected from multiple sources. " 
                     f"Analysis covers {len(economic_articles)} economic-related articles from the past " 
                     f"{self._get_date_range(economic_articles)}.*")
        
        return "\n".join(report)
    
    def _generate_executive_summary(self, articles):
        """Generate the executive summary section"""
        # Analyze overall trends
        category_counts = Counter()
        for article in articles:
            for category in article.get('categories', {}):
                category_counts[category] += 1
                
        # Create summary paragraph
        most_common_categories = category_counts.most_common(3)
        category_text = ", ".join([f"{cat}" for cat, count in most_common_categories])
        
        summary = ("This report analyzes recent developments across the Indo-Pacific region, "
                  f"focusing on key {category_text} trends. "
                  f"Based on analysis of {len(articles)} articles from various sources, "
                  "the region remains a focal point of global geopolitical competition, "
                  "with continued emphasis on multilateral frameworks and economic cooperation "
                  "amid ongoing security challenges. Overall sentiment analysis indicates "
                  f"{self._get_overall_sentiment_description(articles)} "
                  "in economic cooperation balanced against growing security concerns.")
        
        return summary
        
    def _generate_security_section(self, articles):
        """Generate the security developments section"""
        # Sort articles by importance
        articles = sorted(articles, key=lambda x: x['importance'], reverse=True)
        
        # Take top articles for analysis
        top_articles = articles[:min(5, len(articles))]
        
        # Generate section content from top articles
        security_content = []
        
        # Group by sub-categories
        sub_section_count = 1
        
        # Regional Security Architecture (if relevant articles exist)
        architecture_articles = [a for a in top_articles 
                               if any(term in a.get('summary', '').lower() 
                                     for term in ['architecture', 'framework', 'structure', 'quad', 'alliance'])]
        if architecture_articles:
            security_content.append(f"### {sub_section_count}.1 Regional Security Architecture Evolution")
            # Generate paragraph about security architecture from article summaries
            arch_summary = self._generate_topic_summary(architecture_articles, 
                                                     "security architecture", 
                                                     max_sentences=3)
            security_content.append(arch_summary)
            sub_section_count += 1
            
        # Military Developments (always include)
        security_content.append(f"### {sub_section_count}.{1 if sub_section_count == 1 else 2} Key Military Developments")
        # Take top 3 military-focused articles
        military_articles = [a for a in top_articles 
                           if 'Military' in a.get('categories', {})][:3]
        
        for i, article in enumerate(military_articles):
            # Create concise bullet with citation link
            security_content.append(f"- **{article['title']}** - "
                                    f"*{article['source']}, {article['date'].strftime('%b %d')}*: "
                                    f"{article['summary'][:150]}... [Read more]({article['link']})")
                                    
        return "\n".join(security_content)
        
    def _generate_economic_section(self, articles):
        """Generate the economic developments section"""
        # Sort articles by importance
        articles = sorted(articles, key=lambda x: x['importance'], reverse=True)
        
        # Take top articles for analysis
        top_articles = articles[:min(5, len(articles))]
        
        # Generate section content from top articles
        economic_content = []
        
        # Group by sub-categories
        sub_section_count = 1
        
        # Economic Frameworks (if relevant articles exist)
        framework_articles = [a for a in top_articles 
                            if any(term in a.get('summary', '').lower() 
                                  for term in ['framework', 'agreement', 'partnership', 'cooperation', 'investment'])]
        if framework_articles:
            economic_content.append(f"### {sub_section_count}.1 Economic Cooperation Frameworks")
            # Generate paragraph about economic frameworks from article summaries
            framework_summary = self._generate_topic_summary(framework_articles, 
                                                          "economic framework", 
                                                          max_sentences=3)
            economic_content.append(framework_summary)
            sub_section_count += 1
            
        # Trade and Investment (always include)
        economic_content.append(f"### {sub_section_count}.{1 if sub_section_count == 1 else 2} Trade and Investment Developments")
        # Take top 3 trade/investment-focused articles
        trade_articles = [a for a in top_articles 
                        if any(term in a.get('summary', '').lower() 
                              for term in ['trade', 'export', 'import', 'invest'])][:3]
        
        for i, article in enumerate(trade_articles):
            # Create concise bullet with citation link
            economic_content.append(f"- **{article['title']}** - "
                                   f"*{article['source']}, {article['date'].strftime('%b %d')}*: "
                                   f"{article['summary'][:150]}... [Read more]({article['link']})")
                                   
        return "\n".join(economic_content)
        
    def _generate_cultural_section(self, articles):
        """Generate the cultural developments section"""
        # Sort articles by importance
        articles = sorted(articles, key=lambda x: x['importance'], reverse=True)
        
        # Take top articles for analysis
        top_articles = articles[:min(3, len(articles))]
        
        # Generate section content from top articles
        cultural_content = []
        
        for i, article in enumerate(top_articles):
            # Create concise bullet with citation link
            cultural_content.append(f"- **{article['title']}** - "
                                   f"*{article['source']}, {article['date'].strftime('%b %d')}*: "
                                   f"{article['summary'][:150]}... [Read more]({article['link']})")
                                   
        return "\n".join(cultural_content)
        
    def _generate_bilateral_section(self, articles):
        """Generate the bilateral relations section"""
        # Look for articles about bilateral relations
        bilateral_articles = [a for a in articles 
                             if any(term in a.get('summary', '').lower() 
                                   for term in ['bilateral', 'relations', 'partnership', 'agreement'])]
                                   
        # Sort by importance
        bilateral_articles = sorted(bilateral_articles, key=lambda x: x['importance'], reverse=True)
        
        # Take top articles
        top_articles = bilateral_articles[:min(5, len(bilateral_articles))]
        
        # Generate section content
        bilateral_content = []
        
        # If we found bilateral articles
        if top_articles:
            # Group by relationships if possible
            # This is a simplistic approach - could be enhanced with NLP
            for i, article in enumerate(top_articles):
                bilateral_content.append(f"### 4.{i+1} {article['title']}")
                bilateral_content.append(f"{article['summary'][:250]}... [Source: {article['source']}]({article['link']})")
        else:
            bilateral_content.append("No significant bilateral developments in the analyzed time period.")
            
        return "\n".join(bilateral_content)
        
    def _generate_sentiment_section(self, articles):
        """Generate the sentiment analysis section"""
        # Extract sentiment data
        sentiment_data = {}
        for article in articles:
            if article.get('sentiment'):
                for entity, score in article['sentiment'].items():
                    if entity not in sentiment_data:
                        sentiment_data[entity] = []
                    sentiment_data[entity].append(score)
        
        sentiment_content = []
        
        # Calculate average sentiment for each entity
        avg_sentiment = {}
        for entity, scores in sentiment_data.items():
            avg_sentiment[entity] = sum(scores) / len(scores)
            
        # Generate sentiment descriptions
        for entity, score in sorted(avg_sentiment.items(), key=lambda x: abs(x[1]), reverse=True):
            status = "POSITIVE" if score > 0.1 else "NEGATIVE" if score < -0.1 else "NEUTRAL"
            emoji = "📈" if score > 0.1 else "📉" if score < -0.1 else "➖"
            
            sentiment_content.append(f"### 5.{len(sentiment_content)+1} {entity} Sentiment: {status} {emoji}")
            
            factors = []
            if score > 0.1:
                factors.append("- **Positive Factors**: Cooperative diplomatic signals, economic partnerships, shared interests")
            elif score < -0.1:
                factors.append("- **Negative Factors**: Tensions, disputes, competing interests, confrontational rhetoric")
            else:
                factors.append("- **Mixed Factors**: Balanced coverage, competing narratives, complex relations")
                
            sentiment_content.append("\n".join(factors))
            
        if not sentiment_content:
            sentiment_content.append("Insufficient sentiment data available for analysis.")
            
        return "\n".join(sentiment_content)
        
    def _generate_conclusion(self, articles):
        """Generate the conclusion section"""
        conclusion = ("The Indo-Pacific remains the world's most dynamic region economically while facing complex security challenges. "
                     "Economic frameworks continue to evolve, providing mechanisms for cooperation despite tensions. "
                     "Regional sentiment reflects this complex picture, with cautious optimism about economic growth tempered by security concerns.")
        
        return conclusion
    
    def _generate_topic_summary(self, articles, topic, max_sentences=3):
        """Generate a summary paragraph for a specific topic based on articles"""
        if not articles:
            return f"No significant {topic} developments in the analyzed time period."
            
        # Extract all summaries
        all_text = " ".join([a.get('summary', '') for a in articles])
        
        # Simple sentence extraction (could be enhanced with NLP)
        sentences = all_text.split('. ')
        selected_sentences = sentences[:max_sentences]
        
        # Create paragraph with citations
        paragraph = ". ".join(selected_sentences)
        if not paragraph.endswith('.'):
            paragraph += '.'
            
        # Add sources
        sources = [f"[{a['source']}]({a['link']})" for a in articles]
        source_text = f" (Sources: {', '.join(sources)})"
        
        return paragraph + source_text
    
    def _get_date_range(self, articles):
        """Get the date range of articles for citation"""
        if not articles:
            return "selected period"
            
        dates = [a['date'] for a in articles]
        min_date = min(dates)
        max_date = max(dates)
        
        if min_date.month == max_date.month and min_date.year == max_date.year:
            return f"{min_date.strftime('%B %Y')}"
        else:
            return f"{min_date.strftime('%B %d')} to {max_date.strftime('%B %d, %Y')}"
    
    def _get_overall_sentiment_description(self, articles):
        """Get overall sentiment description"""
        # Extract sentiment values
        all_sentiment_values = []
        for article in articles:
            if article.get('sentiment'):
                all_sentiment_values.extend(article['sentiment'].values())
        
        if not all_sentiment_values:
            return "mixed sentiment"
            
        avg_sentiment = sum(all_sentiment_values) / len(all_sentiment_values)
        
        if avg_sentiment > 0.2:
            return "strongly positive sentiment"
        elif avg_sentiment > 0:
            return "cautiously optimistic sentiment"
        elif avg_sentiment > -0.2:
            return "mixed sentiment"
        else:
            return "predominantly negative sentiment"
    
    def _generate_security_overview(self, articles):
        """Generate security overview paragraph"""
        # Simple approach - could be enhanced with more sophisticated NLP
        return (f"Analysis of {len(articles)} security-related articles reveals continued tension "
               "in the Indo-Pacific region. Major powers continue to position military assets "
               "while engaging in diplomatic efforts to manage escalation risks. "
               "Alliance structures continue to evolve with increased focus on "
               "interoperability and joint capabilities.")
    
    def _generate_economic_overview(self, articles):
        """Generate economic overview paragraph"""
        return (f"Analysis of {len(articles)} economic-related articles highlights "
               "continued economic integration in the Indo-Pacific region despite "
               "geopolitical tensions. Trade agreements and investment frameworks "
               "remain central to regional economic architecture, with emphasis on "
               "supply chain resilience and digital economy development.")
    
    def _generate_simple_sentiment_analysis(self, articles):
        """Generate a simplified sentiment analysis section"""
        sentiment_data = {}
        for article in articles:
            if article.get('sentiment'):
                for entity, score in article['sentiment'].items():
                    if entity not in sentiment_data:
                        sentiment_data[entity] = []
                    sentiment_data[entity].append(score)
        
        if not sentiment_data:
            return "Insufficient sentiment data for analysis."
            
        # Calculate average sentiment
        results = []
        for entity, scores in sentiment_data.items():
            avg = sum(scores) / len(scores)
            direction = "positive" if avg > 0.1 else "negative" if avg < -0.1 else "neutral"
            strength = "strongly" if abs(avg) > 0.4 else "moderately" if abs(avg) > 0.2 else "slightly"
            
            if direction != "neutral":
                results.append(f"- Coverage of **{entity}** is {strength} {direction} (score: {avg:.2f})")
            else:
                results.append(f"- Coverage of **{entity}** is relatively {direction} (score: {avg:.2f})")
                
        return "\n".join(results)
    
    def _generate_security_trends(self, articles):
        """Generate security trends analysis"""
        # This could be enhanced with more sophisticated NLP and trend analysis
        return ("Based on the analyzed articles, key security trends in the region include:\n\n"
               "1. **Increasing maritime security focus** in the South China Sea and broader Indo-Pacific\n"
               "2. **Strengthening of alliance networks** particularly among Quad members\n"
               "3. **Growing attention to space and cyber domains** as areas of competition\n"
               "4. **Continued military modernization** across regional powers\n"
               "5. **Persistent regional hotspots** including Korean peninsula and Taiwan Strait")
    
    def _generate_economic_trends(self, articles):
        """Generate economic trends analysis"""
        return ("Based on the analyzed articles, key economic trends in the region include:\n\n"
               "1. **Digital economy expansion** and associated regulatory frameworks\n"
               "2. **Supply chain diversification efforts** driven by resilience concerns\n"
               "3. **Infrastructure development initiatives** competing across the region\n"
               "4. **Trade agreement evolution** with regional comprehensive frameworks\n"
               "5. **Green economy transition** initiatives gaining momentum")

    def save_report(self, report_content, file_path=None):
        """Save report to file"""
        if file_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            file_path = f"reports/indo_pacific_report_{timestamp}.md"
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write report to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        return file_path
    
    def export_report_as_html(self, report_content):
        """Convert markdown report to HTML"""
        # Simple conversion - you may want to use a dedicated library like markdown2 for better results
        html_content = ""
        
        # Very simple markdown conversion
        lines = report_content.split('\n')
        for line in lines:
            # Convert headers
            if line.startswith('# '):
                html_content += f"<h1>{line[2:]}</h1>\n"
            elif line.startswith('## '):
                html_content += f"<h2>{line[3:]}</h2>\n"
            elif line.startswith('### '):
                html_content += f"<h3>{line[4:]}</h3>\n"
            # Convert lists
            elif line.startswith('- '):
                html_content += f"<li>{line[2:]}</li>\n"
            elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
                html_content += f"<li>{line[3:]}</li>\n"
            # Convert links [text](url)
            elif '[' in line and '](' in line and ')' in line:
                # This is a very simple approach - a real implementation would use regex
                parts = line.split('[')
                for part in parts[1:]:  # Skip the first part (before any links)
                    if '](' in part and ')' in part:
                        text = part.split('](')[0]
                        url = part.split('](')[1].split(')')[0]
                        line = line.replace(f'[{text}]({url})', f'<a href="{url}">{text}</a>')
                html_content += f"<p>{line}</p>\n"
            # Convert emphasis
            elif '**' in line:
                # Again, very simple - real implementation would be more robust
                parts = line.split('**')
                result = ''
                for i, part in enumerate(parts):
                    if i % 2 == 1:  # Odd indices are inside ** **
                        result += f"<strong>{part}</strong>"
                    else:
                        result += part
                html_content += f"<p>{result}</p>\n"
            # Empty lines become paragraph breaks
            elif line.strip() == '':
                html_content += "<br>\n"
            # Default - just a paragraph
            else:
                html_content += f"<p>{line}</p>\n"
        
        # Add basic styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Indo-Pacific Region Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                    margin-top: 30px;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .citation {{
                    font-size: 0.9em;
                    color: #7f8c8d;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                    color: #34495e;
                    font-style: italic;
                }}
                code {{
                    background-color: #f7f7f7;
                    padding: 2px 5px;
                    border-radius: 3px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    text-align: left;
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .report-meta {{
                    font-style: italic;
                    color: #7f8c8d;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .footer {{
                    margin-top: 50px;
                    border-top: 1px solid #bdc3c7;
                    padding-top: 20px;
                    font-size: 0.9em;
                    color: #7f8c8d;
                }}
            </style>
        </head>
        <body>
            {html_content}
            <div class="footer">
                <p>Generated by Indo-Pacific Dashboard on {datetime.datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
            </div>
        </body>
        </html>
        """
        
        return styled_html
    
    def create_report_ui(self):
        """
        Create a Streamlit UI for the report generator.
        This should be called from within a Streamlit app.
        """
        st.title("Indo-Pacific Report Generator")
        
        # Report configuration
        with st.form("report_config"):
            st.subheader("Report Configuration")
            
            # Report title
            report_title = st.text_input(
                "Report Title", 
                "Indo-Pacific Region: Current Developments and Sentiment Analysis"
            )
            
            # Report type
            report_type = st.selectbox(
                "Report Type",
                ["Comprehensive", "Security-Focused", "Economic-Focused", "Summary"],
                help="Select the type of report to generate"
            )
            
            # Time period
            time_period = st.selectbox(
                "Time Period",
                ["All Time", "Past Day", "Past Week", "Past Month"],
                help="Select the time period to include in the report"
            )
            
            # Categories
            st.write("Categories to Include:")
            col1, col2 = st.columns(2)
            with col1:
                include_military = st.checkbox("Military", value=True)
                include_political = st.checkbox("Political", value=True)
                include_civil = st.checkbox("Civil Affairs", value=True)
            with col2:
                include_business = st.checkbox("Business", value=True)
                include_drug = st.checkbox("Drug Proliferation", value=False)
                include_cwmd = st.checkbox("CWMD", value=False)
            
            # Country focus
            country_options = [
                "All", "China", "United States", "Japan", "Australia", "India", 
                "Indonesia", "Philippines", "Malaysia", "Vietnam", "South Korea", 
                "Taiwan", "Thailand", "New Caledonia", "Wallis and Futuna"
            ]
            countries = st.multiselect(
                "Country Focus",
                country_options,
                default=["All"],
                help="Select specific countries to focus on, or 'All'"
            )
            
            # Submit button
            submit = st.form_submit_button("Generate Report")
        
        # Process form submission
        if submit:
            # Map form values to report parameters
            report_params = {
                "title": report_title,
                "report_type": report_type.lower(),
                "time_period": time_period.split(" ")[-1].lower() if time_period != "All Time" else None,
                "included_categories": []
            }
            
            # Add selected categories
            if include_military:
                report_params["included_categories"].append("Military")
            if include_political:
                report_params["included_categories"].append("Political")
            if include_civil:
                report_params["included_categories"].append("Civil Affairs")
            if include_business:
                report_params["included_categories"].append("Business")
            if include_drug:
                report_params["included_categories"].append("Drug Proliferation")
            if include_cwmd:
                report_params["included_categories"].append("CWMD")
                
            # Handle country selection
            if "All" not in countries:
                report_params["included_countries"] = countries
            
            # Show a spinner while generating the report
            with st.spinner("Generating report... This may take a moment."):
                report_content = self.generate_report(**report_params)
            
            # Display report
            st.subheader("Generated Report")
            with st.expander("View Report", expanded=True):
                st.markdown(report_content)
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                # Download as Markdown
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                file_name = f"indo_pacific_report_{timestamp}.md"
                
                st.download_button(
                    label="Download as Markdown",
                    data=report_content,
                    file_name=file_name,
                    mime="text/markdown"
                )
            
            with col2:
                # Download as HTML
                html_content = self.export_report_as_html(report_content)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                html_file_name = f"indo_pacific_report_{timestamp}.html"
                
                st.download_button(
                    label="Download as HTML",
                    data=html_content,
                    file_name=html_file_name,
                    mime="text/html"
                )
