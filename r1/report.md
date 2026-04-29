# Interpretation of Charts in R1 Folder

This report provides detailed interpretations of all charts generated in the R1 folder, which analyze Chinese diaspora scholars in higher education research. The charts are categorized by their research themes for better understanding.

## Table of Contents

1. [Author Distribution Charts](#author-distribution-charts)
   1.1 [Geographic Distribution](#geographic-distribution)
   1.2 [Temporal Distribution](#temporal-distribution)

2. [Disciplinary Background Charts](#disciplinary-background-charts)

3. [Institution Affiliation Charts](#institution-affiliation-charts)

4. [Collaboration Pattern Charts](#collaboration-pattern-charts)

5. [Research Focus Charts](#research-focus-charts)

6. [CSV Data Files](#csv-data-files)
   6.1 [Author Information Files](#author-information-files)
   6.2 [Author Productivity Files](#author-productivity-files)
   6.3 [Geographic Distribution Files](#geographic-distribution-files)
   6.4 [Disciplinary Classification Files](#disciplinary-classification-files)
   6.5 [Institution Affiliation Files](#institution-affiliation-files)
   6.6 [Collaboration Analysis Files](#collaboration-analysis-files)

7. [Conclusion](#conclusion)

---

## 1. Author Distribution Charts

### 1.1 Geographic Distribution

#### `author_country_map.html`
- **Chart Type**: Interactive world map
- **Data Source**: `author_countries.csv`, `country_author_counts.csv`
- **Content**: Shows the geographic distribution of all Chinese diaspora scholars across different countries
- **Key Features**: 
  - Uses color coding to represent the number of authors in each country
  - Allows zooming and panning for detailed viewing
  - Displays exact counts when hovering over a country
- **Significance**: Provides a visual overview of the global spread of Chinese diaspora scholars in higher education research

#### `active_author_world_map.html`
- **Chart Type**: Interactive world map
- **Data Source**: `active_author_country_counts.csv`
- **Content**: Focuses specifically on the geographic distribution of highly productive authors
- **Key Features**: 
  - Similar interactive features to the general author map
  - Highlights countries with concentrations of highly productive scholars
- **Significance**: Identifies the global academic hubs where highly productive Chinese diaspora scholars are located

### 1.2 Temporal Distribution

#### `highly_active_authors_trend.html`
- **Chart Type**: Interactive line chart
- **Data Source**: `active_authors_by_period.csv`
- **Content**: Shows the trend of highly productive authors over 5-year periods
- **Key Features**: 
  - X-axis: Time periods (e.g., 2005-2009, 2010-2014, etc.)
  - Y-axis: Number of highly productive authors
  - Interactive tooltips showing exact counts
- **Significance**: Demonstrates the growth of research productivity among Chinese diaspora scholars over time

---

## 2. Disciplinary Background Charts

#### `author_subject_distribution_pie_chart.png`
- **Chart Type**: Static pie chart
- **Data Source**: `subject_category_totals.csv`
- **Content**: Shows the distribution of authors across five disciplinary categories
- **Key Features**: 
  - Categories: Humanities & Social Sciences, Science & Technology, Medicine & Agriculture, Economics & Management, Others
  - Each slice shows the percentage and number of authors
- **Significance**: Illustrates the disciplinary concentration of Chinese diaspora scholars in higher education research

#### `author_subject_distribution.html`
- **Chart Type**: Interactive pie chart
- **Data Source**: `subject_category_totals.csv`
- **Content**: Interactive version of the disciplinary distribution pie chart
- **Key Features**: 
  - Hover effects showing exact counts and percentages
  - Clickable slices for potential filtering
  - Responsive design for different screen sizes
- **Significance**: Provides an interactive way to explore the disciplinary composition of the scholar community

---

## 3. Institution Affiliation Charts

#### `institution_main_category_distribution.png`
- **Chart Type**: Static pie chart
- **Data Source**: `institution_category_stats.csv`
- **Content**: Shows the distribution of authors by their main institution category
- **Key Features**: 
  - Categories: Universities, Research Institutions, Medical Institutions, Enterprises, Others
  - Clear visual representation of the dominance of universities
- **Significance**: Highlights the primary institutional affiliations of Chinese diaspora scholars

#### `institution_all_categories_distribution.png`
- **Chart Type**: Static bar chart
- **Data Source**: `institution_category_stats.csv`
- **Content**: Shows the number of authors across all institution categories
- **Key Features**: 
  - X-axis: Institution categories
  - Y-axis: Number of authors
  - Clear numerical values for each category
- **Significance**: Provides a quantitative comparison of author counts across different institution types

#### `institution_category_distribution.html`
- **Chart Type**: Interactive combined chart
- **Data Source**: `institution_category_stats.csv`
- **Content**: Combines both pie chart and bar chart views of institution category distribution
- **Key Features**: 
  - Toggle between different chart types
  - Interactive tooltips with detailed information
  - Export options for chart images
- **Significance**: Offers flexible visualization options for exploring institution affiliation patterns

---

## 4. Collaboration Pattern Charts

#### `collaboration_rate_comparison.png`
- **Chart Type**: Static bar chart
- **Data Source**: `collaboration_comparison_result.csv`
- **Content**: Compares average collaboration rates between highly productive and low productive authors
- **Key Features**: 
  - Two bars representing the two author groups
  - Clear numerical values for each group's average collaboration rate
- **Significance**: Visualizes the difference in collaboration patterns between highly and low productive authors

#### `collaboration_rate_distribution.png`
- **Chart Type**: Static box plot
- **Data Source**: `collaboration_comparison.csv`
- **Content**: Shows the distribution of collaboration rates for both author groups
- **Key Features**: 
  - Box plots displaying median, quartiles, and outliers
  - Comparison of distribution spread between the two groups
- **Significance**: Reveals the variability in collaboration rates within each author group

#### `collaboration_comparison_report.html`
- **Chart Type**: Interactive dashboard
- **Data Source**: `collaboration_comparison.csv`, `collaboration_comparison_result.csv`
- **Content**: Comprehensive interactive report on collaboration patterns
- **Key Features**: 
  - Multiple chart types (bar charts, box plots, histograms)
  - Filtering options by author group
  - Detailed statistical analysis
- **Significance**: Provides an in-depth interactive exploration of collaboration patterns among Chinese diaspora scholars

#### `papers_comparison.png`
- **Chart Type**: Static bar chart
- **Data Source**: `author_publication_stats.csv`, `highly_productive_scholars.csv`
- **Content**: Compares the number of papers published by different author groups
- **Key Features**: 
  - Comparison between highly productive and low productive authors
  - Clear visual representation of publication output differences
- **Significance**: Highlights the publication productivity gap between different author groups

---

## 5. Research Focus Charts

#### `all_papers_wordcloud.png`
- **Chart Type**: Static word cloud
- **Data Source**: Keywords extracted from all papers in 04_Diaspora_Articles_12195(1).xlsx
- **Content**: Shows the most frequent keywords across all papers
- **Key Features**: 
  - Word size represents frequency
  - Focus on professional terminology only
  - Excludes common words and non-research terms
- **Significance**: Identifies the dominant research topics across all Chinese diaspora scholars

#### `high_productive_authors_wordcloud.png`
- **Chart Type**: Static word cloud
- **Data Source**: Keywords extracted from papers by highly productive authors
- **Content**: Shows the most frequent keywords in papers by highly productive authors
- **Key Features**: 
  - Similar design to the all-papers word cloud
  - Focuses specifically on highly productive authors' research
- **Significance**: Reveals the research focus of the most productive Chinese diaspora scholars

#### `low_productive_authors_wordcloud.png`
- **Chart Type**: Static word cloud
- **Data Source**: Keywords extracted from papers by low productive authors
- **Content**: Shows the most frequent keywords in papers by low productive authors
- **Key Features**: 
  - Similar design to other word clouds
  - Focuses specifically on low productive authors' research
- **Significance**: Identifies the research interests of less productive Chinese diaspora scholars

#### `keyword_wordcloud_analysis.html`
- **Chart Type**: Interactive comparative analysis
- **Data Source**: Keywords from all papers, highly productive authors' papers, and low productive authors' papers
- **Content**: Interactive comparison of keyword distributions across author groups
- **Key Features**: 
  - Side-by-side word cloud displays
  - Frequency tables for top keywords
  - Comparative analysis of research focus
- **Significance**: Provides a comprehensive interactive comparison of research interests across different author groups

---

## 6. CSV Data Files

### Author Information Files

#### `unique_authors.csv`
- **Content**: List of all unique authors extracted from the dataset
- **Columns**: `Author`
- **Key Features**: Contains the complete list of 8,565 unique authors
- **Significance**: Serves as the foundation for all author-related analyses

#### `unique_authors_with_subject.csv`
- **Content**: Authors with their primary disciplinary classification and publication counts by discipline
- **Columns**: `Author`, `Main_Subject`, `Humanities_Social_Science`, `Economics_Management`, `Science_Technology`, `Medicine_Agriculture`, `Other`, `Total_Papers`
- **Key Features**: 
  - Assigns each author to a primary discipline based on their publications
  - Shows publication counts across all discipline categories
- **Significance**: Provides detailed disciplinary information for each author

### Author Productivity Files

#### `author_publication_stats.csv`
- **Content**: Publication statistics for each author
- **Columns**: `Author`, `Total_Papers`, `Year_Range`, `Average_Per_Year`
- **Key Features**: 
  - Shows total papers published by each author
  - Calculates the year range of publications
  - Computes average annual publication rate
- **Significance**: Measures research productivity across all authors

#### `highly_productive_scholars.csv`
- **Content**: List of highly productive authors who published ≥5 papers in any 5-year period
- **Columns**: `Author`, `Articles`, `Year_Range`, `Average`
- **Key Features**: Contains 263 highly productive authors (3.07% of total)
- **Significance**: Identifies the most active researchers in the dataset

#### `active_authors_by_period.csv`
- **Content**: Number of highly productive authors by 5-year period
- **Columns**: `Period`, `ActiveAuthors`
- **Key Features**: Shows the trend of highly productive authors over time
- **Significance**: Demonstrates how research productivity has evolved across different time periods

### Geographic Distribution Files

#### `author_countries.csv`
- **Content**: Mapping of authors to their country(ies) of affiliation
- **Columns**: `Author`, `Country`
- **Key Features**: Handles authors with multiple country affiliations
- **Significance**: Provides the raw data for geographic distribution analysis

#### `country_author_counts.csv`
- **Content**: Count of authors by country
- **Columns**: `Country`, `AuthorCount`
- **Key Features**: Shows the number of authors in each country
- **Significance**: Summarizes the geographic distribution of all authors

#### `active_author_country_counts.csv`
- **Content**: Count of highly productive authors by country
- **Columns**: `Country`, `ActiveAuthorCount`
- **Key Features**: Focuses specifically on highly productive authors
- **Significance**: Identifies countries with the highest concentration of productive researchers

### Disciplinary Classification Files

#### `subject_category_totals.csv`
- **Content**: Summary of authors and papers by disciplinary category
- **Columns**: `Subject_Category`, `Author_Count`, `Total_Papers`
- **Key Features**: Aggregates data across five disciplinary categories
- **Significance**: Shows the overall disciplinary composition of the scholar community

### Institution Affiliation Files

#### `authors_with_institution_categories.csv`
- **Content**: Authors with their main institution and its category
- **Columns**: `Author`, `Main_Institution`, `Institution_Category`
- **Key Features**: Classifies institutions into five categories (Universities, Research Institutions, etc.)
- **Significance**: Provides institutional affiliation information for each author

#### `institution_category_stats.csv`
- **Content**: Summary of authors by institution category
- **Columns**: `Institution_Category`, `Author_Count`
- **Key Features**: Aggregates author counts across institution types
- **Significance**: Shows the distribution of authors by institutional affiliation

### Collaboration Analysis Files

#### `author_collaboration_analysis.csv`
- **Content**: Collaboration analysis for each author
- **Columns**: `Author`, `Total_Papers`, `Collaborative_Papers`, `Collaboration_Rate`
- **Key Features**: 
  - Calculates the number of collaborative papers per author
  - Computes collaboration rate (collaborative papers / total papers)
- **Significance**: Measures individual author collaboration patterns

#### `collaboration_comparison.csv`
- **Content**: Collaboration rates for both highly productive and low productive authors
- **Columns**: `Author`, `Author_Type`, `Collaboration_Rate`
- **Key Features**: Compares collaboration rates between the two author groups
- **Significance**: Provides raw data for collaboration pattern comparison

#### `collaboration_comparison_simple.csv`
- **Content**: Simplified collaboration comparison between author groups
- **Columns**: `Metric`, `Highly_Productive`, `Low_Productive`
- **Key Features**: Shows summary statistics (average, median, etc.) for both groups
- **Significance**: Offers a simplified view of collaboration differences

#### `collaboration_comparison_result.csv`
- **Content**: Final comparison results of collaboration rates
- **Columns**: `Author_Type`, `Average_Collaboration_Rate`, `Median_Collaboration_Rate`
- **Key Features**: Focuses on average and median collaboration rates
- **Significance**: Presents the key findings from the collaboration analysis

---

## Conclusion

The charts and CSV data files in the R1 folder provide a comprehensive analysis of Chinese diaspora scholars in higher education research. They cover multiple dimensions including geographic distribution, disciplinary background, institutional affiliations, collaboration patterns, and research focus. These visualizations and data help us understand:

1. Where these scholars are located globally and how their distribution has changed over time
2. What disciplinary backgrounds they come from
3. What types of institutions they are affiliated with
4. How their collaboration patterns differ based on productivity
5. What research topics they focus on and how these topics vary between different groups

The CSV data files provide the foundation for in-depth analysis, containing detailed information about authors, their productivity, geographic distribution, disciplinary backgrounds, institutional affiliations, and collaboration patterns. The visual charts transform this complex data into intuitive representations that make the research findings more accessible and easier to understand.

Together, these charts and data files offer valuable insights into the characteristics, distribution, and contributions of Chinese diaspora scholars in the field of higher education research.

---

**Report Date**: April 29, 2026
**Data Source**: 04_Diaspora_Articles_12195(1).xlsx and derived datasets
**Analysis Tools**: Python with pandas, matplotlib, wordcloud, and Chart.js
