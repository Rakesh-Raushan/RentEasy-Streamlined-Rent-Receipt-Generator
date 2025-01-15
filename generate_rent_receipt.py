import streamlit as st
from fpdf import FPDF
from datetime import datetime, timedelta
import inflect
import base64
import json
import os
import uuid

# Setup logging directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class RentReceiptGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def generate_receipt(self, date, tenant_name, amount, month, property_address, owner_name, owner_address, owner_pan):
        self.pdf.add_page()
        
        # Add decorative header line
        self.pdf.set_draw_color(0, 0, 128)
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, 10, 200, 10)
        
        # Add header
        self.pdf.set_font("Arial", style="B", size=16)
        self.pdf.set_text_color(0, 0, 128)
        self.pdf.cell(200, 15, txt="HOUSE RENT RECEIPT", ln=True, align="C")
        
        # Reset text color
        self.pdf.set_text_color(0, 0, 0)
        
        # Add receipt number and date in a box
        self.pdf.set_fill_color(240, 240, 250)
        self.pdf.rect(10, 30, 190, 15, style='F')
        self.pdf.set_font("Arial", style="B", size=12)
        self.pdf.set_xy(10, 32)
        self.pdf.cell(190, 10, txt=f"Date: {date}", align="R")

        # Add main content section
        self.pdf.ln(20)
        
        # Receipt details
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

    def number_to_words(self, num):
        p = inflect.engine()
        return p.number_to_words(num, andword="").capitalize()

    def get_pdf_bytes(self):
        return self.pdf.output(dest='S').encode('latin-1')

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

def save_usage_log(config_data):
    """Save the configuration to a JSON file in the logs directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"receipt_config_{timestamp}_{unique_id}.json"
    
    # Add metadata to the config
    config_data["generated_at"] = timestamp
    config_data["request_id"] = unique_id
    
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(config_data, f, indent=4)
    
    return filename

def main():
    st.set_page_config(page_title="Rent Receipt Generator", layout="wide")
    
    # Add title and description
    st.title("🏠 Rent Receipt Generator")
    st.markdown("""
    Generate professional rent receipts easily. Fill in the details below and download your receipts in PDF format.
    """)
    
    # Create two columns for input fields
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tenant Details")
        tenant_name = st.text_input("Tenant Name")
        amount = st.number_input("Monthly Rent Amount (₹)", min_value=0, step=1000)
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        property_address = st.text_area("Property Address")

    with col2:
        st.subheader("Owner Details")
        owner_name = st.text_input("Owner Name")
        owner_address = st.text_area("Owner Address")
        owner_pan = st.text_input("Owner PAN")

    if st.button("Generate Receipts"):
        if all([tenant_name, amount, property_address, owner_name, owner_address, owner_pan]):
            try:
                # Prepare config data for logging
                config_data = {
                    "tenant_name": tenant_name,
                    "amount": amount,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "property_address": property_address,
                    "owner_name": owner_name,
                    "owner_address": owner_address,
                    "owner_pan": owner_pan
                }
                
                # Save usage log
                log_filename = save_usage_log(config_data)
                
                # Generate receipts
                months = generate_month_range(config_data["start_date"], config_data["end_date"])
                generator = RentReceiptGenerator()

                for month in months:
                    month_start_date = datetime.strptime(f"01 {month}", "%d %B %Y").strftime("%d/%m/%Y")
                    generator.generate_receipt(
                        month_start_date, tenant_name, amount, month, property_address,
                        owner_name, owner_address, owner_pan
                    )

                # Get PDF bytes and create download button
                pdf_bytes = generator.get_pdf_bytes()
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                
                # Create download button
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Rent_Receipts.pdf">📥 Download Rent Receipts PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success(f"✅ Rent receipts generated successfully!")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in all the required fields.")

if __name__ == "__main__":
    main()