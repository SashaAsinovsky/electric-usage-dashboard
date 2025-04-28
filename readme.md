# ⚡ Electric Usage Analytics Dashboard

A data visualization tool for analyzing electricity usage, costs, and rates over time (1998-2020).

![Dashboard Preview](https://github.com/yourusername/electric-usage-dashboard/assets/preview.png)

## Features

- 🔌 **Interactive Visualizations**: Dynamic charts for usage, cost, and rate analysis
- 💲 **Cost Analysis**: Track spending patterns and identify cost-saving opportunities
- 📈 **Rate Tracking**: Monitor electricity rates and their impact on overall costs
- 📊 **Year-over-Year Comparisons**: Visualize annual changes and identify trends
- 🔍 **Intelligent Insights**: Automated analysis of patterns and anomalies
- 📱 **Responsive Design**: Optimized for both desktop and mobile viewing
- 🌙 **Dark Theme**: Electric-themed dark mode visualization

## Live Demo

You can view the live dashboard at: [https://yourusername-electric-usage-dashboard.streamlit.app](https://yourusername-electric-usage-dashboard.streamlit.app)

## Running Locally

To run this dashboard locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/electric-usage-dashboard.git
   cd electric-usage-dashboard
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to http://localhost:8501

## Deploying to Streamlit Cloud

This repository is ready for deployment on Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Create a new app, selecting this repository
5. Choose `app.py` as the main file
6. Deploy!

## Data Structure

The dashboard visualizes the following data:
- Annual electricity usage (kWh)
- Annual electricity costs ($)
- Cost per kilowatt-hour ($/kWh)
- Year-over-year changes in usage, cost, and rates

## Customization

To use with your own data, modify the `data` list in the `ElectricUsageDashboard` class in `app.py`.

## Technologies Used

- [Streamlit](https://streamlit.io/): Web application framework
- [Plotly](https://plotly.com/): Interactive charts and visualizations
- [Pandas](https://pandas.pydata.org/): Data manipulation and analysis
- [NumPy](https://numpy.org/): Numerical computing

## License

MIT

## Contact

For questions or feedback, please open an issue on this repository.

---

This project is distinct from the water usage dashboard and features a completely different visual style with an electric-themed dark mode interface.
