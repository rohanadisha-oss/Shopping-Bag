import datetime
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# ReportLab Imports for Professional PDF Generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PDFShoppingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Shopping List to PDF")
        self.root.geometry("420x750")

        self.COLORS = {
            "bg": "#0f172a",
            "card_bg": "#1e293b",
            "text": "#ffffff",
            "subtext": "#94a3b8",
            "primary": "#3b82f6",
            "accent": "#10b981",
            "danger": "#f43f5e",
            "input_bg": "#020617",
            "border": "#334155",
        }

        self.root.configure(bg=self.COLORS["bg"])
        self.items_data = []

        self._build_ui()

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.COLORS["bg"], pady=12)
        header_frame.pack(fill="x", padx=16)

        title = tk.Label(
            header_frame,
            text="Smart Shopping List",
            font=("sans-serif", 18, "bold"),
            fg=self.COLORS["text"],
            bg=self.COLORS["bg"],
            anchor="w",
        )
        title.pack(fill="x")

        now = datetime.datetime.now()
        self.date_str = now.strftime("%d %b %Y | %I:%M %p")

        lbl_date = tk.Label(
            header_frame,
            text=f"Date: {self.date_str}",
            font=("sans-serif", 10),
            fg=self.COLORS["primary"],
            bg=self.COLORS["bg"],
            anchor="w",
        )
        lbl_date.pack(fill="x", pady=(2, 0))

        # Input Card
        self.card_input = tk.Frame(
            self.root,
            bg=self.COLORS["card_bg"],
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLORS["border"],
        )
        self.card_input.pack(fill="x", padx=16, pady=(0, 10))

        c1_top = tk.Frame(self.card_input, bg=self.COLORS["card_bg"])
        c1_top.pack(fill="x", padx=12, pady=(10, 5))

        lbl1 = tk.Label(
            c1_top,
            text="1. Write Items (one per line)",
            font=("sans-serif", 11, "bold"),
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
        )
        lbl1.pack(side="left")

        btn_clear = tk.Button(
            c1_top,
            text="Clear",
            font=("sans-serif", 9, "bold"),
            fg=self.COLORS["danger"],
            bg=self.COLORS["card_bg"],
            bd=0,
            command=lambda: self.txt_input.delete("1.0", tk.END),
        )
        btn_clear.pack(side="right")

        self.txt_input = tk.Text(
            self.card_input,
            height=4,
            font=("sans-serif", 12),
            bg=self.COLORS["input_bg"],
            fg=self.COLORS["text"],
            insertbackground="white",
            bd=0,
            padx=10,
            pady=8,
            wrap="word",
        )
        self.txt_input.pack(fill="x", padx=12, pady=(0, 10))
        self.txt_input.insert("1.0", "Rice (5 kg)\nMilk (1 Liter)\nEggs (12 Pcs)")

        btn_submit = tk.Button(
            self.card_input,
            text="Create List  -->",
            font=("sans-serif", 11, "bold"),
            bg=self.COLORS["primary"],
            fg="white",
            bd=0,
            pady=8,
            command=self.lock_and_build_list,
        )
        btn_submit.pack(fill="x", padx=12, pady=(0, 12))

        # Selection Card
        self.card_list = tk.Frame(
            self.root,
            bg=self.COLORS["card_bg"],
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.COLORS["border"],
        )
        self.card_list.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        c2_top = tk.Frame(self.card_list, bg=self.COLORS["card_bg"])
        c2_top.pack(fill="x", padx=12, pady=(10, 5))

        lbl2 = tk.Label(
            c2_top,
            text="2. Select & Enter Prices",
            font=("sans-serif", 11, "bold"),
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
        )
        lbl2.pack(side="left")

        self.btn_edit = tk.Button(
            c2_top,
            text="[Edit Items]",
            font=("sans-serif", 9, "bold"),
            fg=self.COLORS["subtext"],
            bg=self.COLORS["card_bg"],
            bd=0,
            command=self.show_input_card,
        )

        self.items_container = tk.Frame(
            self.card_list, bg=self.COLORS["card_bg"]
        )
        self.items_container.pack(fill="both", expand=True, padx=12, pady=5)

        # PDF Export Button
        self.btn_pdf = tk.Button(
            self.root,
            text="📄 Generate & Download PDF Bill",
            font=("sans-serif", 12, "bold"),
            bg=self.COLORS["accent"],
            fg="white",
            bd=0,
            pady=12,
            command=self.generate_pdf_invoice,
        )
        self.btn_pdf.pack(fill="x", padx=16, pady=(0, 16))

        self.lock_and_build_list()

    def show_input_card(self):
        self.card_input.pack(
            fill="x", padx=16, pady=(0, 10), before=self.card_list
        )
        self.btn_edit.pack_forget()

    def lock_and_build_list(self):
        raw_text = self.txt_input.get("1.0", tk.END).strip()
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

        if not lines:
            messagebox.showwarning("Warning", "Please write at least one item!")
            return

        self.card_input.pack_forget()
        self.btn_edit.pack(side="right")

        for widget in self.items_container.winfo_children():
            widget.destroy()

        self.items_data = []

        for line in lines:
            row_frame = tk.Frame(
                self.items_container, bg=self.COLORS["card_bg"], pady=4
            )
            row_frame.pack(fill="x")

            var_check = tk.BooleanVar(value=True)

            cb = tk.Checkbutton(
                row_frame,
                text=line,
                variable=var_check,
                font=("sans-serif", 12),
                fg=self.COLORS["text"],
                bg=self.COLORS["card_bg"],
                selectcolor=self.COLORS["input_bg"],
                anchor="w",
            )
            cb.pack(side="left", fill="x", expand=True)

            lbl_currency = tk.Label(
                row_frame,
                text="Rs.",
                font=("sans-serif", 10, "bold"),
                fg=self.COLORS["subtext"],
                bg=self.COLORS["card_bg"],
            )
            lbl_currency.pack(side="left", padx=(5, 2))

            price_entry = tk.Entry(
                row_frame,
                width=7,
                font=("sans-serif", 11, "bold"),
                bg=self.COLORS["input_bg"],
                fg=self.COLORS["accent"],
                insertbackground="white",
                bd=1,
                relief="solid",
                justify="center",
            )
            price_entry.pack(side="right", padx=(0, 5))
            price_entry.insert(0, "0")

            self.items_data.append(
                {
                    "name": line,
                    "selected": var_check,
                    "price_entry": price_entry,
                }
            )

    def generate_pdf_invoice(self):
        """Generates a PDF document with ReportLab."""
        selected_items = []
        total_amount = 0.0

        for item in self.items_data:
            if item["selected"].get():
                try:
                    price = float(item["price_entry"].get().strip())
                except ValueError:
                    price = 0.0

                selected_items.append((item["name"], f"Rs. {price:.2f}"))
                total_amount += price

        if not selected_items:
            messagebox.showinfo("Notice", "No items selected to create a PDF!")
            return

        # Target Path in Android Download Folder
        download_dir = "/sdcard/Download"
        if not os.path.exists(download_dir):
            download_dir = os.getcwd()

        filename = (
            f"Invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        pdf_path = os.path.join(download_dir, filename)

        try:
            # Build Professional PDF Layout
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30,
            )
            story = []

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "TitleStyle",
                parent=styles["Heading1"],
                fontName="Helvetica-Bold",
                fontSize=22,
                textColor=colors.HexColor("#1e293b"),
                spaceAfter=6,
            )
            meta_style = ParagraphStyle(
                "MetaStyle",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=10,
                textColor=colors.HexColor("#64748b"),
                spaceAfter=15,
            )

            # Header Section
            story.append(Paragraph("OFFICIAL INVOICE / RECEIPT", title_style))
            story.append(
                Paragraph(
                    f"<b>Date:</b> {self.date_str} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Invoice ID:</b> #INV-{datetime.datetime.now().strftime('%M%S')}",
                    meta_style,
                )
            )
            story.append(Spacer(1, 10))

            # Table Content
            table_data = [["Item Description", "Price (INR)"]]
            for name, price_str in selected_items:
                table_data.append([name, price_str])

            table_data.append(["TOTAL AMOUNT", f"Rs. {total_amount:.2f}"])

            # Styling the Table
            invoice_table = Table(table_data, colWidths=[350, 150])
            invoice_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        (
                            "BACKGROUND",
                            (0, 1),
                            (-1, -2),
                            colors.HexColor("#f8fafc"),
                        ),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                        ("FONTSIZE", (0, -1), (-1, -1), 12),
                        (
                            "BACKGROUND",
                            (0, -1),
                            (-1, -1),
                            colors.HexColor("#10b981"),
                        ),
                        ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
                        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ]
                )
            )

            story.append(invoice_table)
            doc.build(story)

            messagebox.showinfo(
                "PDF Created!", f"Your PDF bill was saved to:\n\n{pdf_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "PDF Generation Error", f"Could not create PDF:\n{str(e)}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFShoppingApp(root)
    root.mainloop()
