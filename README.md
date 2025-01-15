# 🏠 Rent Receipt Generator

A streamlined web application that generates professional rent receipts in PDF format. Built with Streamlit and Python, this tool makes it easy to create multiple rent receipts for any date range.

## Features

- 📝 Generate multiple rent receipts in a single PDF
- 📅 Select custom date ranges
- 💰 Automatic amount-to-words conversion
- 🎨 Professional and clean design
- 📱 Responsive web interface
- 🔢 Receipt generation counter

## Demo

You can access the live application at: [RentEasy-Generate-rent-receipts](https://renteasy-streamlined-rent-receipt-generator.streamlit.app/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/rent-receipt-generator.git
cd rent-receipt-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application locally:
```bash
streamlit run app.py
```

2. Open your web browser and go to `http://localhost:8501`

3. Fill in the required information:
   - Tenant Details (name, rent amount, dates, property address)
   - Owner Details (name, address, PAN)

4. Click "Generate Receipts" and download your PDF

## Requirements

- Python 3.7+
- Streamlit
- FPDF
- inflect

See `requirements.txt` for all dependencies.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Run tests (if available)
python -m pytest
```

## Deployment

This application can be deployed on Streamlit Cloud for free:

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Login with your GitHub account
4. Deploy the application
5. Your app will be live at `https://your-app-name.streamlit.app`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- PDF generation using [FPDF](https://pyfpdf.readthedocs.io/en/latest/)
- Number to words conversion using [inflect](https://pypi.org/project/inflect/)

## Support

If you find any bugs or have feature suggestions, please create an issue in the GitHub repository.