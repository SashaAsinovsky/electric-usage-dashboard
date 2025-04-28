import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration - using a dark theme for electric visualization
st.set_page_config(
    page_title="Electric Usage Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for electric theme
st.markdown("""
<style>
    /* Main theme colors - electric theme with purples and blues */
    :root {
        --main-bg-color: #1a1a2e;
        --secondary-bg: #16213e;
        --accent-color: #7b2cbf;
        --accent-light: #c77dff;
        --text-color: #e6e6e6;
        --grid-color: rgba(123, 44, 191, 0.15);
    }
    
    /* Overall page styling */
    .main {
        background-color: var(--main-bg-color);
        color: var(--text-color);
    }
    
    h1, h2, h3 {
        color: var(--accent-light);
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.8rem;
        color: var(--accent-light);
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--accent-color);
        text-shadow: 0 0 10px rgba(199, 125, 255, 0.5);
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: var(--accent-light);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Card styling for sections */
    .card {
        background-color: var(--secondary-bg);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--accent-color);
    }
    
    /* Metric cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background-color: #231942;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        text-align: center;
        border: 1px solid var(--accent-color);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(123, 44, 191, 0.3);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #c77dff;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 8px rgba(199, 125, 255, 0.3);
    }
    
    .metric-label {
        font-size: 1rem;
        color: #e6e6e6;
        margin-bottom: 0.5rem;
    }
    
    .metric-trend {
        font-size: 0.9rem;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        display: inline-block;
    }
    
    .trend-up {
        background-color: rgba(255, 87, 87, 0.2);
        color: #ff5757;
    }
    
    .trend-down {
        background-color: rgba(0, 212, 128, 0.2);
        color: #00d480;
    }
    
    .trend-neutral {
        background-color: rgba(255, 255, 255, 0.1);
        color: #cccccc;
    }
    
    /* Insights section */
    .insight-item {
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.8rem;
        background-color: rgba(123, 44, 191, 0.1);
        border-radius: 0.5rem;
        border-left: 3px solid var(--accent-color);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--accent-color);
        color: var(--text-color);
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Make the Streamlit tabs more attractive */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: var(--secondary-bg);
        border-radius: 8px 8px 0px 0px;
        gap: 1px;
        padding: 10px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-color);
        color: white;
    }

    /* Style for the sidebar */
    .css-1d391kg, .css-hxt7ib {
        background-color: var(--secondary-bg);
    }
    
    /* Style for radio buttons and checkboxes */
    .stRadio > div, .stCheckbox > div {
        background-color: var(--secondary-bg);
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Create our Electric Usage Dashboard class
class ElectricUsageDashboard:
    def __init__(self):
        # Initialize the data
        self.data = [
            {"year": 1998, "totalUsage": 4765600, "totalCost": 423102.07, "costPerKwh": 0.08878, "usageChange": 0, "costChange": 0, "rateChange": 0},
            {"year": 1999, "totalUsage": 7673400, "totalCost": 671438.68, "costPerKwh": 0.0875, "usageChange": 61, "costChange": 58.7, "rateChange": -1.4},
            {"year": 2000, "totalUsage": 7786800, "totalCost": 676049.56, "costPerKwh": 0.08682, "usageChange": 1.5, "costChange": 0.7, "rateChange": -0.8},
            {"year": 2001, "totalUsage": 7840000, "totalCost": 690162.8, "costPerKwh": 0.08803, "usageChange": 0.7, "costChange": 2.1, "rateChange": 1.4},
            {"year": 2002, "totalUsage": 8703800, "totalCost": 683468.49, "costPerKwh": 0.07853, "usageChange": 11, "costChange": -1, "rateChange": -10.8},
            {"year": 2003, "totalUsage": 9065000, "totalCost": 749578.02, "costPerKwh": 0.08269, "usageChange": 4.1, "costChange": 9.7, "rateChange": 5.3},
            {"year": 2004, "totalUsage": 9366000, "totalCost": 772713.61, "costPerKwh": 0.0825, "usageChange": 3.3, "costChange": 3.1, "rateChange": -0.2},
            {"year": 2005, "totalUsage": 8947400, "totalCost": 850074.84, "costPerKwh": 0.09501, "usageChange": -4.5, "costChange": 10, "rateChange": 15.2},
            {"year": 2006, "totalUsage": 8850800, "totalCost": 843114.19, "costPerKwh": 0.09526, "usageChange": -1.1, "costChange": -0.8, "rateChange": 0.3},
            {"year": 2007, "totalUsage": 8869301, "totalCost": 830936.51, "costPerKwh": 0.09369, "usageChange": 0.2, "costChange": -1.4, "rateChange": -1.6},
            {"year": 2008, "totalUsage": 8490312, "totalCost": 825909.05, "costPerKwh": 0.09728, "usageChange": -4.3, "costChange": -0.6, "rateChange": 3.8},
            {"year": 2009, "totalUsage": 8026327, "totalCost": 542203.96, "costPerKwh": 0.06755, "usageChange": -5.5, "costChange": -34.4, "rateChange": -30.6},
            {"year": 2010, "totalUsage": 8046772, "totalCost": 564842.44, "costPerKwh": 0.07019, "usageChange": 0.3, "costChange": 4.2, "rateChange": 3.9},
            {"year": 2011, "totalUsage": 8091665, "totalCost": 494064.46, "costPerKwh": 0.06106, "usageChange": 0.6, "costChange": -12.5, "rateChange": -13},
            {"year": 2012, "totalUsage": 8080384, "totalCost": 480434.92, "costPerKwh": 0.05946, "usageChange": -0.1, "costChange": -2.8, "rateChange": -2.6},
            {"year": 2013, "totalUsage": 8061741, "totalCost": 588484.89, "costPerKwh": 0.073, "usageChange": -0.2, "costChange": 22.5, "rateChange": 22.8},
            {"year": 2014, "totalUsage": 8140087, "totalCost": 683455, "costPerKwh": 0.08, "usageChange": 1, "costChange": 16.1, "rateChange": 9.6},
            {"year": 2015, "totalUsage": 8750364, "totalCost": 560007, "costPerKwh": 0.06, "usageChange": 7.5, "costChange": -18.1, "rateChange": -25},
            {"year": 2016, "totalUsage": 8697231, "totalCost": 460245, "costPerKwh": 0.05, "usageChange": -0.6, "costChange": -17.8, "rateChange": -16.7},
            {"year": 2017, "totalUsage": 8255345, "totalCost": 425453, "costPerKwh": 0.05, "usageChange": -5.1, "costChange": -7.6, "rateChange": 0},
            {"year": 2018, "totalUsage": 8636427, "totalCost": 475236, "costPerKwh": 0.06, "usageChange": 4.6, "costChange": 11.7, "rateChange": 20},
            {"year": 2019, "totalUsage": 8418866, "totalCost": 419129, "costPerKwh": 0.05, "usageChange": -2.5, "costChange": -11.8, "rateChange": -16.7},
            {"year": 2020, "totalUsage": 6754261, "totalCost": 327728, "costPerKwh": 0.05, "usageChange": -19.8, "costChange": -21.8, "rateChange": 0}
        ]
        
        # Convert to DataFrame for easier manipulation
        self.df = pd.DataFrame(self.data)
        
        # Calculate statistics
        self.stats = self.calculate_stats()
    
    def calculate_stats(self):
        """Calculate key statistics from the data"""
        stats = {}
        
        # Basic statistics
        stats['total_usage'] = self.df['totalUsage'].sum()
        stats['avg_usage'] = self.df['totalUsage'].mean()
        stats['total_cost'] = self.df['totalCost'].sum()
        stats['avg_cost'] = self.df['totalCost'].mean()
        stats['avg_rate'] = self.df['costPerKwh'].mean()
        
        # Max and min values
        stats['max_usage'] = self.df['totalUsage'].max()
        stats['max_usage_year'] = int(self.df.loc[self.df['totalUsage'].idxmax(), 'year'])
        
        stats['min_usage'] = self.df['totalUsage'].min()
        stats['min_usage_year'] = int(self.df.loc[self.df['totalUsage'].idxmin(), 'year'])
        
        stats['max_cost'] = self.df['totalCost'].max()
        stats['max_cost_year'] = int(self.df.loc[self.df['totalCost'].idxmax(), 'year'])
        
        stats['min_cost'] = self.df['totalCost'].min()
        stats['min_cost_year'] = int(self.df.loc[self.df['totalCost'].idxmin(), 'year'])
        
        stats['max_rate'] = self.df['costPerKwh'].max()
        stats['max_rate_year'] = int(self.df.loc[self.df['costPerKwh'].idxmax(), 'year'])
        
        stats['min_rate'] = self.df['costPerKwh'].min()
        stats['min_rate_year'] = int(self.df.loc[self.df['costPerKwh'].idxmin(), 'year'])
        
        # Long-term trends
        first_year = self.df.iloc[0]
        last_year = self.df.iloc[-1]
        
        stats['usage_change_pct'] = ((last_year['totalUsage'] - first_year['totalUsage']) / first_year['totalUsage']) * 100
        stats['cost_change_pct'] = ((last_year['totalCost'] - first_year['totalCost']) / first_year['totalCost']) * 100
        stats['rate_change_pct'] = ((last_year['costPerKwh'] - first_year['costPerKwh']) / first_year['costPerKwh']) * 100
        
        # Largest single-year changes
        stats['max_usage_increase'] = self.df['usageChange'].max()
        stats['max_usage_increase_year'] = int(self.df.loc[self.df['usageChange'].idxmax(), 'year'])
        
        stats['max_usage_decrease'] = self.df['usageChange'].min()
        stats['max_usage_decrease_year'] = int(self.df.loc[self.df['usageChange'].idxmin(), 'year'])
        
        stats['max_cost_increase'] = self.df['costChange'].max()
        stats['max_cost_increase_year'] = int(self.df.loc[self.df['costChange'].idxmax(), 'year'])
        
        stats['max_cost_decrease'] = self.df['costChange'].min()
        stats['max_cost_decrease_year'] = int(self.df.loc[self.df['costChange'].idxmin(), 'year'])
        
        # Correlation between usage and cost
        stats['usage_cost_correlation'] = self.df['totalUsage'].corr(self.df['totalCost'])
        
        return stats
    
    def format_number(self, num):
        """Format large numbers with commas"""
        return f"{int(num):,}"
    
    def format_currency(self, num):
        """Format currency values"""
        return f"${num:,.2f}"
    
    def format_rate(self, num):
        """Format rate values (cost per kWh)"""
        return f"${num:.5f}"
    
    def format_percent(self, num):
        """Format percentage values"""
        return f"{num:.1f}%"
    
    def render_dashboard(self):
        """Main method to render the entire dashboard"""
        # Add dashboard title
        st.markdown('<h1 class="main-header">⚡ Electric Usage Analytics Dashboard</h1>', unsafe_allow_html=True)
        
        # Get options from sidebar
        show_trend, normalize_data, year_range = self.render_sidebar()
        
        # Filter data based on selected years
        filtered_df = self.df[(self.df['year'] >= year_range[0]) & (self.df['year'] <= year_range[1])].copy()
        
        # Apply normalization if selected (convert kWh to MWh)
        if normalize_data:
            filtered_df['normalizedUsage'] = filtered_df['totalUsage'] / 1000  # convert to MWh
        
        # Display KPI metrics
        self.render_kpi_metrics(filtered_df)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔌 Usage & Cost", 
            "💲 Cost Analysis", 
            "📈 Rate Trends",
            "📊 Year-over-Year", 
            "📋 Data Table"
        ])
        
        with tab1:
            self.render_usage_cost_view(filtered_df, show_trend, normalize_data)
        
        with tab2:
            self.render_cost_analysis(filtered_df, show_trend)
        
        with tab3:
            self.render_rate_analysis(filtered_df, show_trend)
        
        with tab4:
            self.render_year_over_year(filtered_df)
        
        with tab5:
            self.render_data_table(filtered_df, normalize_data)
        
        # Display insights and analysis
        st.markdown('<h2 class="sub-header">Key Insights & Patterns</h2>', unsafe_allow_html=True)
        self.render_insights(filtered_df)
        
        # Footer
        st.markdown('<div class="footer">⚡ Electric Usage Analytics Dashboard • Created with Streamlit • Data from 1998-2020</div>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with controls"""
        st.sidebar.title("Dashboard Controls")
        
        # Add electric-themed icon
        st.sidebar.markdown("# ⚡")
        
        st.sidebar.markdown("### Data Range")
        
        # Year range slider
        min_year = int(self.df['year'].min())
        max_year = int(self.df['year'].max())
        selected_years = st.sidebar.slider(
            "Select Years",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        st.sidebar.markdown(f"🗓️ Selected period: {selected_years[0]} - {selected_years[1]}")
        st.sidebar.markdown("---")
        
        # Analysis options
        st.sidebar.markdown("### Display Options")
        
        show_trend = st.sidebar.checkbox("Show trend lines", value=True)
        normalize_data = st.sidebar.checkbox("Show usage in MWh (÷1000)", value=False)
        
        if normalize_data:
            st.sidebar.info("📊 Displaying usage in Megawatt-hours (MWh) instead of Kilowatt-hours (kWh) for better readability.")
        
        if show_trend:
            st.sidebar.info("📈 Trend lines show the general direction of the data over time, helping identify long-term patterns.")
        
        st.sidebar.markdown("---")
        
        # About this dashboard
        st.sidebar.markdown("### About")
        st.sidebar.markdown("""
        This dashboard visualizes electricity usage and cost data from 1998 to 2020, providing insights into:
        
        - Usage patterns and trends
        - Cost analysis
        - Rate fluctuations
        - Year-over-year comparisons
        
        Use the controls above to customize the visualization.
        """)
        
        return show_trend, normalize_data, selected_years
    
    def render_kpi_metrics(self, df):
        """Render key performance indicator cards"""
        st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
        
        # Calculate metrics for filtered data
        latest_year = df.iloc[-1]['year']
        prev_year_idx = df.index[-2] if len(df) > 1 else df.index[-1]
        latest_usage = df.iloc[-1]['totalUsage']
        latest_cost = df.iloc[-1]['totalCost']
        latest_rate = df.iloc[-1]['costPerKwh']
        
        # Usage change vs previous year
        usage_change = 0
        if len(df) > 1:
            usage_change = ((df.iloc[-1]['totalUsage'] - df.iloc[-2]['totalUsage']) / df.iloc[-2]['totalUsage']) * 100
        
        # Cost change vs previous year
        cost_change = 0
        if len(df) > 1:
            cost_change = ((df.iloc[-1]['totalCost'] - df.iloc[-2]['totalCost']) / df.iloc[-2]['totalCost']) * 100
        
        # Rate change vs previous year
        rate_change = 0
        if len(df) > 1:
            rate_change = ((df.iloc[-1]['costPerKwh'] - df.iloc[-2]['costPerKwh']) / df.iloc[-2]['costPerKwh']) * 100
        
        # Total usage in period
        total_usage = df['totalUsage'].sum()
        avg_usage = df['totalUsage'].mean()
        
        # Render metric cards using custom HTML/CSS
        
        # Card 1: Latest Annual Usage
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{self.format_number(latest_usage)}</div>
            <div class="metric-label">Annual Usage in {latest_year} (kWh)</div>
            <div class="metric-trend {'trend-down' if usage_change < 0 else 'trend-up' if usage_change > 0 else 'trend-neutral'}">
                {self.format_percent(usage_change)} vs Previous Year
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Card 2: Latest Annual Cost
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{self.format_currency(latest_cost)}</div>
            <div class="metric-label">Annual Cost in {latest_year}</div>
            <div class="metric-trend {'trend-down' if cost_change < 0 else 'trend-up' if cost_change > 0 else 'trend-neutral'}">
                {self.format_percent(cost_change)} vs Previous Year
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Card 3: Latest Rate
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{self.format_rate(latest_rate)}</div>
            <div class="metric-label">Cost per kWh in {latest_year}</div>
            <div class="metric-trend {'trend-down' if rate_change < 0 else 'trend-up' if rate_change > 0 else 'trend-neutral'}">
                {self.format_percent(rate_change)} vs Previous Year
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Card 4: Average Annual Usage
        avg_vs_latest = ((latest_usage - avg_usage) / avg_usage) * 100
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{self.format_number(avg_usage)}</div>
            <div class="metric-label">Average Annual Usage (kWh)</div>
            <div class="metric-trend {'trend-down' if avg_vs_latest < 0 else 'trend-up' if avg_vs_latest > 0 else 'trend-neutral'}">
                {self.format_percent(avg_vs_latest)} vs Average
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_usage_cost_view(self, df, show_trend=False, normalize_data=False):
        """Render the combined usage and cost view"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Usage and Cost Comparison</h3>', unsafe_allow_html=True)
        
        # Determine which column to use based on normalize setting
        usage_col = 'normalizedUsage' if normalize_data and 'normalizedUsage' in df.columns else 'totalUsage'
        usage_title = 'Usage (MWh)' if normalize_data else 'Usage (kWh)'
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add bars for usage
        fig.add_trace(
            go.Bar(
                x=df['year'], 
                y=df[usage_col], 
                name="Electricity Usage",
                marker_color='#9d4edd',
                opacity=0.85,
                hovertemplate=f'Year: %{{x}}<br>{usage_title}: %{{y:,.0f}}<extra></extra>'
            ),
            secondary_y=False
        )
        
        # Add line for cost
        fig.add_trace(
            go.Scatter(
                x=df['year'], 
                y=df['totalCost'], 
                name="Total Cost",
                mode='lines+markers',
                line=dict(color='#5390d9', width=3),
                marker=dict(size=8, color='#5390d9'),
                hovertemplate='Year: %{x}<br>Cost: $%{y:,.2f}<extra></extra>'
            ),
            secondary_y=True
        )
        
        # Add trendlines if requested
        if show_trend:
            # Usage trendline
            z = np.polyfit(df['year'], df[usage_col], 1)
            y_fit = np.polyval(z, df['year'])
            
            fig.add_trace(
                go.Scatter(
                    x=df['year'],
                    y=y_fit,
                    mode='lines',
                    line=dict(color='rgba(157, 78, 221, 0.5)', width=2, dash='dash'),
                    name='Usage Trend',
                    hoverinfo='skip'
                ),
                secondary_y=False
            )
            
            # Cost trendline
            z_cost = np.polyfit(df['year'], df['totalCost'], 1)
            y_cost_fit = np.polyval(z_cost, df['year'])
            
            fig.add_trace(
                go.Scatter(
                    x=df['year'],
                    y=y_cost_fit,
                    mode='lines',
                    line=dict(color='rgba(83, 144, 217, 0.5)', width=2, dash='dash'),
                    name='Cost Trend',
                    hoverinfo='skip'
                ),
                secondary_y=True
            )
        
        # Update the layout
        fig.update_layout(
            title="Annual Electricity Usage and Cost",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500,
            plot_bgcolor='rgba(22, 33, 62, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6e6'),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        # Configure axes
        fig.update_xaxes(
            title_text="Year",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickmode='linear',
            dtick=1 if len(df) < 15 else 2
        )
        
        fig.update_yaxes(
            title_text=usage_title,
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickformat=",",
            secondary_y=False
        )
        
        fig.update_yaxes(
            title_text="Cost ($)",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickprefix="$",
            tickformat=",",
            secondary_y=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add some insights about the relationship between usage and cost
        correlation = df['totalUsage'].corr(df['totalCost'])
        
        st.markdown(f"""
        <div class="insight-item">
            <strong>Correlation between usage and cost: {correlation:.2f}</strong> - 
            {'A strong positive correlation indicates costs generally rise with usage.' if correlation > 0.7 else 
             'A moderate correlation suggests other factors besides usage affect cost.' if correlation > 0.4 else
             'A weak correlation indicates cost is largely independent of usage.'}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_cost_analysis(self, df, show_trend=False):
        """Render the cost analysis view"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Cost Analysis</h3>', unsafe_allow_html=True)
        
        # Create area chart for cost
        fig = go.Figure()
        
        # Add area chart for cost
        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df['totalCost'],
                mode='lines',
                fill='tozeroy',
                name='Total Cost',
                line=dict(color='#5390d9', width=3),
                fillcolor='rgba(83, 144, 217, 0.3)',
                hovertemplate='Year: %{x}<br>Cost: $%{y:,.2f}<extra></extra>'
            )
        )
        
        # Add trendline if requested
        if show_trend:
            z = np.polyfit(df['year'], df['totalCost'], 1)
            y_fit = np.polyval(z, df['year'])
            
            fig.add_trace(
                go.Scatter(
                    x=df['year'],
                    y=y_fit,
                    mode='lines',
                    line=dict(color='rgba(255, 255, 255, 0.6)', width=2, dash='dash'),
                    name='Cost Trend',
                    hoverinfo='skip'
                )
            )
        
        # Update the layout
        fig.update_layout(
            title="Annual Electricity Cost",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500,
            plot_bgcolor='rgba(22, 33, 62, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6e6'),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        # Configure axes
        fig.update_xaxes(
            title_text="Year",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickmode='linear',
            dtick=1 if len(df) < 15 else 2
        )
        
        fig.update_yaxes(
            title_text="Cost ($)",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickprefix="$",
            tickformat=","
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate key metrics for the filtered data
        max_cost = df['totalCost'].max()
        max_cost_year = int(df.loc[df['totalCost'].idxmax(), 'year'])
        min_cost = df['totalCost'].min()
        min_cost_year = int(df.loc[df['totalCost'].idxmin(), 'year'])
        
        # First and last year in the filtered dataset
        first_year = df.iloc[0]['year']
        last_year = df.iloc[-1]['year']
        first_cost = df.iloc[0]['totalCost']
        last_cost = df.iloc[-1]['totalCost']
        pct_change = ((last_cost - first_cost) / first_cost) * 100
        
        # Add insights about cost
        st.markdown(f"""
        <div class="insight-item">
            <strong>Highest cost: {self.format_currency(max_cost)} in {max_cost_year}</strong> - 
            {'This peak represents a significant outlier compared to other years.' if max_cost > df['totalCost'].mean() * 1.5 else
             'This represents the peak expenditure in the selected period.'}
        </div>
        
        <div class="insight-item">
            <strong>Lowest cost: {self.format_currency(min_cost)} in {min_cost_year}</strong> - 
            {'This demonstrates a substantial cost saving opportunity compared to peak years.' if max_cost > min_cost * 1.5 else
             'The difference between peak and minimum costs is relatively modest.'}
        </div>
        
        <div class="insight-item">
            <strong>Long-term trend: {self.format_percent(pct_change)} from {first_year} to {last_year}</strong> - 
            {'Costs have increased significantly over this period.' if pct_change > 20 else
             'Costs have decreased significantly over this period.' if pct_change < -20 else
             'Costs have remained relatively stable over this period.'}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_rate_analysis(self, df, show_trend=False):
        """Render the rate analysis view"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Rate Analysis (Cost per kWh)</h3>', unsafe_allow_html=True)
        
        # Create line chart for rate
        fig = go.Figure()
        
        # Add line chart for rate
        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df['costPerKwh'],
                mode='lines+markers',
                name='Cost per kWh',
                line=dict(color='#7b2cbf', width=3),
                marker=dict(size=8, color='#7b2cbf'),
                hovertemplate='Year: %{x}<br>Rate: $%{y:.5f} per kWh<extra></extra>'
            )
        )
        
        # Add trendline if requested
        if show_trend:
            z = np.polyfit(df['year'], df['costPerKwh'], 1)
            y_fit = np.polyval(z, df['year'])
            
            fig.add_trace(
                go.Scatter(
                    x=df['year'],
                    y=y_fit,
                    mode='lines',
                    line=dict(color='rgba(255, 255, 255, 0.6)', width=2, dash='dash'),
                    name='Rate Trend',
                    hoverinfo='skip'
                )
            )
        
        # Add threshold line for average
        avg_rate = df['costPerKwh'].mean()
        fig.add_shape(
            type="line",
            x0=df['year'].min(),
            x1=df['year'].max(),
            y0=avg_rate,
            y1=avg_rate,
            line=dict(
                color="rgba(255, 255, 255, 0.5)",
                width=1,
                dash="dot",
            )
        )
        
        fig.add_annotation(
            x=df['year'].min() + 1,
            y=avg_rate,
            text=f"Avg: ${avg_rate:.5f}",
            showarrow=False,
            font=dict(color="rgba(255, 255, 255, 0.8)"),
            bgcolor="rgba(123, 44, 191, 0.5)",
            bordercolor="rgba(123, 44, 191, 0.8)",
            borderwidth=1,
            borderpad=4,
            xanchor="left"
        )
        
        # Update the layout
        fig.update_layout(
            title="Electricity Rate Over Time",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500,
            plot_bgcolor='rgba(22, 33, 62, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6e6'),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        # Configure axes
        fig.update_xaxes(
            title_text="Year",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickmode='linear',
            dtick=1 if len(df) < 15 else 2
        )
        
        fig.update_yaxes(
            title_text="Cost per kWh ($)",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickprefix="$",
            tickformat=".5f"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate key metrics for the filtered data
        max_rate = df['costPerKwh'].max()
        max_rate_year = int(df.loc[df['costPerKwh'].idxmax(), 'year'])
        min_rate = df['costPerKwh'].min()
        min_rate_year = int(df.loc[df['costPerKwh'].idxmin(), 'year'])
        
        # First and last year in the filtered dataset
        first_year = df.iloc[0]['year']
        last_year = df.iloc[-1]['year']
        first_rate = df.iloc[0]['costPerKwh']
        last_rate = df.iloc[-1]['costPerKwh']
        pct_change = ((last_rate - first_rate) / first_rate) * 100
        
        # Add insights about rates
        st.markdown(f"""
        <div class="insight-item">
            <strong>Highest rate: {self.format_rate(max_rate)} per kWh in {max_rate_year}</strong> - 
            {'This peak rate represents a significant increase from average rates.' if max_rate > avg_rate * 1.3 else
             'This peak rate is higher but not dramatically different from average rates.'}
        </div>
        
        <div class="insight-item">
            <strong>Lowest rate: {self.format_rate(min_rate)} per kWh in {min_rate_year}</strong> - 
            {'This represents a substantial cost advantage compared to peak rates.' if max_rate > min_rate * 1.5 else
             'The difference between peak and minimum rates is relatively modest.'}
        </div>
        
        <div class="insight-item">
            <strong>Long-term trend: {self.format_percent(pct_change)} from {first_year} to {last_year}</strong> - 
            {'Rates have increased significantly over this period.' if pct_change > 20 else
             'Rates have decreased significantly over this period.' if pct_change < -20 else
             'Rates have remained relatively stable over this period.'}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_year_over_year(self, df):
        """Render the year-over-year changes"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Year-over-Year Changes</h3>', unsafe_allow_html=True)
        
        # Need at least 2 years of data for comparison
        if len(df) < 2:
            st.warning("At least 2 years of data are needed for year-over-year analysis.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Create figure for year-over-year changes
        fig = go.Figure()
        
        # Add usage change bars
        fig.add_trace(
            go.Bar(
                x=df['year'][1:],  # Skip first year as it has no previous year for comparison
                y=df['usageChange'][1:],
                name="Usage Change %",
                marker_color='#9d4edd',
                hovertemplate='Year: %{x}<br>Usage Change: %{y:.1f}%<extra></extra>'
            )
        )
        
        # Add cost change bars
        fig.add_trace(
            go.Bar(
                x=df['year'][1:],
                y=df['costChange'][1:],
                name="Cost Change %",
                marker_color='#5390d9',
                hovertemplate='Year: %{x}<br>Cost Change: %{y:.1f}%<extra></extra>'
            )
        )
        
        # Add rate change bars
        fig.add_trace(
            go.Bar(
                x=df['year'][1:],
                y=df['rateChange'][1:],
                name="Rate Change %",
                marker_color='#c77dff',
                hovertemplate='Year: %{x}<br>Rate Change: %{y:.1f}%<extra></extra>'
            )
        )
        
        # Add zero line
        fig.add_shape(
            type="line",
            x0=df['year'].min(),
            x1=df['year'].max(),
            y0=0,
            y1=0,
            line=dict(
                color="rgba(255, 255, 255, 0.5)",
                width=1,
                dash="solid",
            )
        )
        
        # Update the layout
        fig.update_layout(
            title="Year-over-Year Percentage Changes",
            hovermode="x unified",
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500,
            plot_bgcolor='rgba(22, 33, 62, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6e6'),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        # Configure axes
        fig.update_xaxes(
            title_text="Year",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            tickmode='linear',
            dtick=1 if len(df) < 15 else 2
        )
        
        fig.update_yaxes(
            title_text="Change (%)",
            gridcolor='rgba(123, 44, 191, 0.15)',
            tickfont=dict(size=12),
            ticksuffix="%"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Find the most dramatic changes
        if len(df) > 1:
            max_usage_increase = df['usageChange'][1:].max()
            max_usage_increase_year = int(df.loc[df['usageChange'].idxmax(), 'year']) if not pd.isna(df['usageChange'].idxmax()) else None
            
            max_usage_decrease = df['usageChange'][1:].min()
            max_usage_decrease_year = int(df.loc[df['usageChange'].idxmin(), 'year']) if not pd.isna(df['usageChange'].idxmin()) else None
            
            max_cost_increase = df['costChange'][1:].max()
            max_cost_increase_year = int(df.loc[df['costChange'].idxmax(), 'year']) if not pd.isna(df['costChange'].idxmax()) else None
            
            max_cost_decrease = df['costChange'][1:].min()
            max_cost_decrease_year = int(df.loc[df['costChange'].idxmin(), 'year']) if not pd.isna(df['costChange'].idxmin()) else None
            
            # Add insights about dramatic changes
            st.markdown(f"""
            <div class="insight-item">
                <strong>Most significant usage increase: {self.format_percent(max_usage_increase)} in {max_usage_increase_year}</strong> - 
                {'This represents an unusual surge in electricity consumption.' if max_usage_increase > 15 else
                 'This indicates a moderate increase in electricity demand.'}
            </div>
            
            <div class="insight-item">
                <strong>Most significant usage decrease: {self.format_percent(max_usage_decrease)} in {max_usage_decrease_year}</strong> - 
                {'This represents a dramatic reduction in electricity consumption.' if max_usage_decrease < -15 else
                 'This indicates a moderate decrease in electricity demand.'}
            </div>
            
            <div class="insight-item">
                <strong>Most significant cost increase: {self.format_percent(max_cost_increase)} in {max_cost_increase_year}</strong> - 
                {'This spike in costs had a major impact on overall expenses.' if max_cost_increase > 20 else
                 'This increase in costs is notable but not extreme.'}
            </div>
            
            <div class="insight-item">
                <strong>Most significant cost decrease: {self.format_percent(max_cost_decrease)} in {max_cost_decrease_year}</strong> - 
                {'This dramatic cost reduction represents potential savings opportunities.' if max_cost_decrease < -20 else
                 'This decrease in costs provided some budget relief.'}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_data_table(self, df, normalize_data=False):
        """Render the data table view"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Data Table</h3>', unsafe_allow_html=True)
        
        # Create a copy of the dataframe for display
        display_df = df.copy()
        
        # Format columns for display
        display_df['totalUsage'] = display_df['totalUsage'].apply(self.format_number)
        display_df['totalCost'] = display_df['totalCost'].apply(self.format_currency)
        display_df['costPerKwh'] = display_df['costPerKwh'].apply(self.format_rate)
        
        # Format percentage columns
        for col in ['usageChange', 'costChange', 'rateChange']:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%" if not pd.isna(x) else "N/A")
        
        # If normalized data is available, include it
        if normalize_data and 'normalizedUsage' in display_df.columns:
            display_df['normalizedUsage'] = display_df['normalizedUsage'].apply(lambda x: f"{x:,.0f}")
            
            # Rename columns
            display_df = display_df.rename(columns={
                'year': 'Year',
                'totalUsage': 'Usage (kWh)',
                'normalizedUsage': 'Usage (MWh)',
                'totalCost': 'Total Cost',
                'costPerKwh': 'Cost per kWh',
                'usageChange': 'Usage Change (%)',
                'costChange': 'Cost Change (%)',
                'rateChange': 'Rate Change (%)'
            })
        else:
            # Rename columns
            display_df = display_df.rename(columns={
                'year': 'Year',
                'totalUsage': 'Usage (kWh)',
                'totalCost': 'Total Cost',
                'costPerKwh': 'Cost per kWh',
                'usageChange': 'Usage Change (%)',
                'costChange': 'Cost Change (%)',
                'rateChange': 'Rate Change (%)'
            })
        
        # Display the table
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )
        
        # Add download button for CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚡ Download Data as CSV",
            data=csv,
            file_name="electric_usage_data.csv",
            mime="text/csv",
            help="Download the complete dataset as a CSV file"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_insights(self, df):
        """Render insights and analysis about the data"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create columns for insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4>Usage Patterns</h4>', unsafe_allow_html=True)
            
            # Calculate long-term trends
            first_year = df.iloc[0]
            last_year = df.iloc[-1]
            pct_change_usage = ((last_year['totalUsage'] - first_year['totalUsage']) / first_year['totalUsage']) * 100
            
            # Create insights about usage
            st.markdown(f"""
            <div class="insight-item">
                <strong>Long-term usage trend:</strong> {'Increasing' if pct_change_usage > 5 else 'Decreasing' if pct_change_usage < -5 else 'Stable'} 
                ({self.format_percent(pct_change_usage)} over {last_year['year'] - first_year['year']} years)
            </div>
            
            <div class="insight-item">
                <strong>Peak usage year:</strong> {int(df.loc[df['totalUsage'].idxmax(), 'year'])} with {self.format_number(df['totalUsage'].max())} kWh
            </div>
            
            <div class="insight-item">
                <strong>Recent usage vs peak:</strong> {self.format_percent(((last_year['totalUsage'] / df['totalUsage'].max()) - 1) * 100)} compared to peak
            </div>
            """, unsafe_allow_html=True)
            
            if len(df) > 5:
                # Detect any obvious patterns
                recent_trend = df.iloc[-5:]['totalUsage'].pct_change().mean() * 100
                st.markdown(f"""
                <div class="insight-item">
                    <strong>Recent 5-year trend:</strong> {'Increasing' if recent_trend > 1 else 'Decreasing' if recent_trend < -1 else 'Stable'} 
                    (avg {self.format_percent(recent_trend)} per year)
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h4>Cost Insights</h4>', unsafe_allow_html=True)
            
            # Calculate cost trends
            pct_change_cost = ((last_year['totalCost'] - first_year['totalCost']) / first_year['totalCost']) * 100
            pct_change_rate = ((last_year['costPerKwh'] - first_year['costPerKwh']) / first_year['costPerKwh']) * 100
            
            # Usage vs cost comparison
            usage_cost_ratio = pct_change_usage / pct_change_cost if pct_change_cost != 0 else 0
            
            # Create insights about costs
            st.markdown(f"""
            <div class="insight-item">
                <strong>Cost per kWh trend:</strong> {'Increasing' if pct_change_rate > 5 else 'Decreasing' if pct_change_rate < -5 else 'Stable'} 
                ({self.format_percent(pct_change_rate)} over {last_year['year'] - first_year['year']} years)
            </div>
            
            <div class="insight-item">
                <strong>Usage vs cost changes:</strong> {'Usage changes outpace cost changes' if abs(usage_cost_ratio) > 1.2 and usage_cost_ratio > 0 else
                                                      'Cost changes outpace usage changes' if abs(usage_cost_ratio) < 0.8 and usage_cost_ratio > 0 else
                                                      'Usage decreases while costs increase' if usage_cost_ratio < 0 and pct_change_usage < 0 and pct_change_cost > 0 else
                                                      'Usage increases while costs decrease' if usage_cost_ratio < 0 and pct_change_usage > 0 and pct_change_cost < 0 else
                                                      'Usage and cost changes are proportional'}
            </div>
            
            <div class="insight-item">
                <strong>Cost volatility:</strong> {'High' if df['costChange'].std() > 15 else 'Moderate' if df['costChange'].std() > 7 else 'Low'} 
                (std dev: {df['costChange'].std():.1f}%)
            </div>
            """, unsafe_allow_html=True)
            
            if len(df) > 5:
                # Analyze recent cost trends
                recent_cost_trend = df.iloc[-5:]['totalCost'].pct_change().mean() * 100
                recent_rate_trend = df.iloc[-5:]['costPerKwh'].pct_change().mean() * 100
                
                st.markdown(f"""
                <div class="insight-item">
                    <strong>Recent cost trend:</strong> {'Increasing' if recent_cost_trend > 1 else 'Decreasing' if recent_cost_trend < -1 else 'Stable'} 
                    (avg {self.format_percent(recent_cost_trend)} per year)
                </div>
                """, unsafe_allow_html=True)
        
        # Add an overall interpretation of the data
        st.markdown('<h4>Summary Analysis</h4>', unsafe_allow_html=True)
        
        # Calculate efficiency - has the rate of usage relative to cost improved?
        first_year_efficiency = first_year['totalCost'] / first_year['totalUsage']
        last_year_efficiency = last_year['totalCost'] / last_year['totalUsage']
        efficiency_change = ((last_year_efficiency - first_year_efficiency) / first_year_efficiency) * 100
        
        # Overall insights
        correlation = df['totalUsage'].corr(df['totalCost'])
        
        st.markdown(f"""
        <div class="insight-item">
            <strong>Overall efficiency change:</strong> {'Improved' if efficiency_change < -5 else 'Worsened' if efficiency_change > 5 else 'Remained stable'}
            ({self.format_percent(-efficiency_change)} over {last_year['year'] - first_year['year']} years)
        </div>
        
        <div class="insight-item">
            <strong>Usage-cost relationship:</strong> {
                'Strong correlation between usage and cost suggests billing is primarily usage-based.' if correlation > 0.7 else
                'Moderate correlation suggests other factors besides usage significantly affect cost.' if correlation > 0.4 else
                'Weak correlation indicates cost is largely independent of usage, suggesting fixed costs or rate changes are dominant factors.'
            }
        </div>
        
        <div class="insight-item">
            <strong>Cost-saving opportunities:</strong> {
                'Significant decreases in usage have not always led to proportional cost savings, suggesting investigating rate structures could yield benefits.' 
                    if pct_change_usage < -10 and pct_change_cost > pct_change_usage else
                'Cost per kWh has increased significantly over time, suggesting exploring alternative rate plans or energy efficiency measures.' 
                    if pct_change_rate > 15 else
                'Usage patterns show opportunities for potential load shifting or demand management to reduce costs.' 
                    if df['usageChange'].std() > 10 else
                'Relatively stable usage and costs suggest focusing on long-term efficiency measures for gradual improvements.'
            }
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# Run the dashboard
if __name__ == "__main__":
    dashboard = ElectricUsageDashboard()
    dashboard.render_dashboard()
