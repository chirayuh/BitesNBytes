# Bites & Bytes 🍰

A personal finance management web application built with **Streamlit** and **Firebase** to track income and expenses efficiently.

## Overview

Bites & Bytes is a multi-page Streamlit application that helps users manage their financial records. The app allows users to add, view, and analyze their income and expense transactions with visual statistics and detailed records.

## Features

### 🏠 Home Page
- **Add Income/Expense Records**: Easily record new transactions with date, amount, and category
- **Quick Transaction Entry**: Intuitive form interface for adding financial records
- **Firebase Integration**: All data is automatically saved to Firestore database

### 💰 Display Income Page
- View all income records in a structured table format
- Filter and sort income transactions
- Track income sources and amounts

### 💸 Display Expense Page
- View all expense records in a detailed table
- Monitor spending patterns
- Categorize and track various expense types

### 📊 Stats Page
- **Visual Analytics**: Charts and graphs for income vs expense analysis
- **Statistical Insights**: Key metrics and trends
- **Data Visualization**: Matplotlib-powered visualizations
- **Summary Statistics**: Total income, total expenses, and net balance

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Python web app framework
- **Backend**: [Firebase](https://firebase.google.com/) - Cloud database and authentication
  - Firestore - NoSQL database for storing transactions
  - Firebase Admin SDK - Server-side Firebase integration
- **Data Processing**: [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis
- **Visualization**: [Matplotlib](https://matplotlib.org/) - Charts and graphs

## Project Structure

```
BitesNBytes/
├── Home.py                          # Main home page with transaction entry
├── pages/
│   ├── 1_Display_Income.py         # Income records display page
│   ├── 2_Display_Expense.py        # Expense records display page
│   └── 3_Stats.py                  # Statistics and analytics page
├── firebaseSetup.py                 # Firebase configuration and testing
├── utils.py                         # Utility functions
├── requirements.txt                 # Python dependencies
├── bitesbytes-f2302-e345b2788029.json  # Firebase credentials
├── images/                          # Application images and assets
└── README.md                        # Project documentation
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the repository**
   ```bash
   cd BitesNBytes
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Firebase**
   - Place your Firebase service account JSON file in the project root
   - Update the filename in `Home.py` and other files if needed (currently: `bitesbytes-f2302-e345b2788029.json`)

4. **Run the application**
   ```bash
   streamlit run Home.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`

## Usage

### Adding a Transaction
1. Go to the Home page
2. Enter the date of the transaction
3. Input the amount
4. Select the category (Income or Expense)
5. Click "Add" to save the transaction

### Viewing Records
- **Income**: Navigate to "Display Income" page to see all income transactions
- **Expenses**: Navigate to "Display Expense" page to see all expense transactions

### Analyzing Statistics
- Go to "Stats" page to view:
  - Income vs Expense comparison charts
  - Statistical summaries
  - Visual analytics and trends

## Dependencies

- `streamlit` - Web app framework
- `firebase-admin` - Firebase backend integration
- `matplotlib` - Data visualization
- `pandas` - Data analysis and manipulation

See `requirements.txt` for specific versions.

## Database Schema

### BitsNBytes Collection
Each transaction document contains:
- **Date**: Date of the transaction
- **Amount**: Transaction amount
- **Category**: Type (Income or Expense)
- Additional metadata from Firestore

## Future Enhancements

- User authentication and multi-user support
- Budget planning and alerts
- Category-wise breakdown and analysis
- Export functionality (CSV, PDF)
- Mobile app version
- Recurring transaction support
- Budget vs Actual comparison

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the application.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

---

**Created with ❤️ using Streamlit and Firebase**
