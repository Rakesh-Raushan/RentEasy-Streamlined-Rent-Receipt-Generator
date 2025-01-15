from fpdf import FPDF
import json
from datetime import datetime, timedelta
import inflect

class RentReceiptGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def generate_receipt(self, date, tenant_name, amount, month, property_address, owner_name, owner_address, owner_pan):
        self.pdf.add_page()
        
        # Add decorative header line
        self.pdf.set_draw_color(0, 0, 128)  # Navy blue color
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, 10, 200, 10)
        
        # Add header: House Rent Receipt
        self.pdf.set_font("Arial", style="B", size=16)
        self.pdf.set_text_color(0, 0, 128)  # Navy blue color
        self.pdf.cell(200, 15, txt="HOUSE RENT RECEIPT", ln=True, align="C")
        
        # Reset text color to black
        self.pdf.set_text_color(0, 0, 0)
        
        # Add receipt number and date in a box
        self.pdf.set_fill_color(240, 240, 250)  # Light blue background
        self.pdf.rect(10, 30, 190, 15, style='F')
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.set_xy(10, 32)
        self.pdf.cell(190, 10, txt=f"Date: {date}", align="R")

        # Add main content section
        self.pdf.ln(20)
        
        # Receipt details in a structured format
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.cell(50, 10, txt="Received From:", ln=0)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(140, 10, txt=tenant_name, ln=1)
        
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.cell(50, 10, txt="Amount:", ln=0)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(140, 10, txt=f"Rs. {amount:,}/-", ln=1)
        
        self.pdf.set_font("Arial", style="I", size=11)
        self.pdf.cell(50, 10, txt="", ln=0)
        self.pdf.cell(140, 10, txt=f"(Rupees {self.number_to_words(amount)} only)", ln=1)
        
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.cell(50, 10, txt="For Month:", ln=0)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(140, 10, txt=month, ln=1)
        
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.cell(50, 10, txt="Property:", ln=0)
        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(140, 10, txt=property_address)

        # Add owner's details in a box
        self.pdf.ln(10)
        self.pdf.set_fill_color(240, 240, 250)
        self.pdf.rect(10, self.pdf.get_y(), 190, 45, style='F')
        
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.cell(190, 10, txt="Owner's Details:", ln=1)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(190, 10, txt=f"Name: {owner_name}", ln=1)
        self.pdf.cell(190, 10, txt=f"Address: {owner_address}", ln=1)
        self.pdf.cell(190, 10, txt=f"PAN: {owner_pan}", ln=1)

        # Add signature section
        self.pdf.ln(20)
        self.pdf.line(20, self.pdf.get_y(), 80, self.pdf.get_y())
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.cell(60, 10, txt="Signature", ln=1)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(60, 10, txt=f"({owner_name})", ln=1)
        
        # # Add footer line
        # self.pdf.set_draw_color(0, 0, 128)
        # self.pdf.line(10, 275, 200, 275)
        # self.pdf.set_font("Arial", style="I", size=8)
        # self.pdf.set_xy(10, 278)
        # self.pdf.cell(190, 5, txt="This is a computer-generated receipt and does not require physical signature.", align="C")

    def number_to_words(self, num):
        p = inflect.engine()
        return p.number_to_words(num, andword="").capitalize()

    def save_pdf(self, filename):
        self.pdf.output(filename)
        print(f"Rent receipts saved as {filename}")

def generate_month_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start
    months = []
    while current <= end:
        months.append(current.strftime("%B %Y"))
        current += timedelta(days=32)
        current = current.replace(day=1)
    return months

def main():
    # Load JSON config
    with open("config.json", "r") as file:
        config = json.load(file)

    tenant_name = config["tenant_name"]
    amount = config["amount"]
    start_date = config["start_date"]
    end_date = config["end_date"]
    property_address = config["property_address"]
    owner_name = config["owner_name"]
    owner_address = config["owner_address"]
    owner_pan = config["owner_pan"]

    months = generate_month_range(start_date, end_date)
    generator = RentReceiptGenerator()

    # Generate all receipts in a single PDF
    for month in months:
        month_start_date = datetime.strptime(f"01 {month}", "%d %B %Y").strftime("%d/%m/%Y")
        generator.generate_receipt(
            month_start_date, tenant_name, amount, month, property_address, 
            owner_name, owner_address, owner_pan
        )

    # Save all receipts in a single PDF
    output_filename = f"Rent_Receipts_{start_date}_to_{end_date}.pdf"
    generator.save_pdf(output_filename)

if __name__ == "__main__":
    main()