import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os

class DataAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("数据统计工具 - LAR与良率计算")
        self.root.geometry("600x500")
        self.root.configure(padx=20, pady=20)
        
        self.filepath = None
        self.data = None
        
        self.setup_ui()

    def setup_ui(self):
        # File selection section
        file_frame = ttk.LabelFrame(self.root, text="第一步：选择数据文件", padding=(10, 10))
        file_frame.pack(fill="x", pady=(0, 15))
        
        self.file_label = ttk.Label(file_frame, text="未选择文件", foreground="gray")
        self.file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="浏览...", command=self.load_file)
        browse_btn.pack(side="right")
        
        # Filter condition section
        filter_frame = ttk.LabelFrame(self.root, text="第二步：设置筛选条件", padding=(10, 10))
        filter_frame.pack(fill="x", pady=(0, 15))
        
        # Part Number (料号)
        part_no_frame = ttk.Frame(filter_frame)
        part_no_frame.pack(fill="x", pady=5)
        ttk.Label(part_no_frame, text="料号列名:").pack(side="left", padx=(0, 5))
        self.col_part_no = ttk.Combobox(part_no_frame, width=15, state="readonly")
        self.col_part_no.pack(side="left", padx=(0, 15))
        
        ttk.Label(part_no_frame, text="目标料号:").pack(side="left", padx=(0, 5))
        self.val_part_no = ttk.Entry(part_no_frame, width=20)
        self.val_part_no.pack(side="left", fill="x", expand=True)
        
        # Period (周期)
        period_frame = ttk.Frame(filter_frame)
        period_frame.pack(fill="x", pady=5)
        ttk.Label(period_frame, text="周期列名:").pack(side="left", padx=(0, 5))
        self.col_period = ttk.Combobox(period_frame, width=15, state="readonly")
        self.col_period.pack(side="left", padx=(0, 15))
        
        ttk.Label(period_frame, text="目标周期:").pack(side="left", padx=(0, 5))
        self.val_period = ttk.Entry(period_frame, width=20)
        self.val_period.pack(side="left", fill="x", expand=True)
        
        # Calculation parameters section
        calc_frame = ttk.LabelFrame(self.root, text="第三步：设置计算列 (需为数值)", padding=(10, 10))
        calc_frame.pack(fill="x", pady=(0, 15))
        
        # Total qty
        tot_frame = ttk.Frame(calc_frame)
        tot_frame.pack(fill="x", pady=5)
        ttk.Label(tot_frame, text="总数/投入量 列:").pack(side="left", padx=(0, 5))
        self.col_total = ttk.Combobox(tot_frame, width=20, state="readonly")
        self.col_total.pack(side="left", fill="x", expand=True)
        
        # Pass qty
        pass_frame = ttk.Frame(calc_frame)
        pass_frame.pack(fill="x", pady=5)
        ttk.Label(pass_frame, text="合格数/产出量 列:").pack(side="left", padx=(0, 5))
        self.col_pass = ttk.Combobox(pass_frame, width=20, state="readonly")
        self.col_pass.pack(side="left", fill="x", expand=True)
        
        # Action button
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", pady=10)
        calc_btn = ttk.Button(action_frame, text="开始计算", command=self.calculate_metrics)
        calc_btn.pack(side="right")
        
        # Results section
        result_frame = ttk.LabelFrame(self.root, text="计算结果", padding=(10, 10))
        result_frame.pack(fill="both", expand=True)
        
        self.result_text = tk.Text(result_frame, height=8, wrap="word", state="disabled")
        self.result_text.pack(fill="both", expand=True)

    def load_file(self):
        filetypes = (
            ('Excel 文件', '*.xlsx *.xls'),
            ('CSV 文件', '*.csv'),
            ('所有文件', '*.*')
        )
        
        filepath = filedialog.askopenfilename(
            title='选择数据表格',
            initialdir='/',
            filetypes=filetypes
        )
        
        if not filepath:
            return
            
        try:
            # Read file based on extension
            _, ext = os.path.splitext(filepath)
            if ext.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(filepath)
            elif ext.lower() == '.csv':
                self.data = pd.read_csv(filepath)
            else:
                messagebox.showerror("错误", "不支持的文件格式，请选择 Excel 或 CSV 文件。")
                return
                
            self.filepath = filepath
            filename = os.path.basename(filepath)
            row_count = len(self.data)
            self.file_label.config(text=f"{filename} (共 {row_count} 行数据)", foreground="black")
            
            # Update comboboxes with column names
            columns = list(self.data.columns)
            self.col_part_no['values'] = ["--不使用--"] + columns
            self.col_part_no.current(0)
            
            self.col_period['values'] = ["--不使用--"] + columns
            self.col_period.current(0)
            
            # Only numeric columns for total and pass
            numeric_cols = list(self.data.select_dtypes(include=['number']).columns)
            all_cols = ["--请选择--"] + columns
            
            self.col_total['values'] = all_cols
            self.col_total.current(0)
            
            self.col_pass['values'] = all_cols
            self.col_pass.current(0)
            
            self.log_result(f"成功加载文件: {filename}\n包含 {row_count} 行, {len(columns)} 列。")
            
        except Exception as e:
            messagebox.showerror("读取错误", f"读取文件时发生错误:\n{str(e)}")

    def calculate_metrics(self):
        if self.data is None:
            messagebox.showwarning("提示", "请先选择数据文件。")
            return
            
        # Get selected columns
        col_pn = self.col_part_no.get()
        col_pd = self.col_period.get()
        col_tot = self.col_total.get()
        col_pas = self.col_pass.get()
        
        # Validation
        if col_tot == "--请选择--" or col_pas == "--请选择--":
            messagebox.showwarning("提示", "必须选择总数和合格数列才能进行计算。")
            return
            
        # Ensure selected columns exist in dataframe
        if col_tot not in self.data.columns or col_pas not in self.data.columns:
            messagebox.showerror("错误", "所选的计算列在数据中不存在。")
            return
            
        # Start filtering
        df_filtered = self.data.copy()
        filter_desc = []
        
        # Filter by Part Number if specified
        if col_pn != "--不使用--":
            target_pn = self.val_part_no.get().strip()
            if target_pn:
                # Convert to string to avoid type mismatch during comparison
                df_filtered = df_filtered[df_filtered[col_pn].astype(str) == target_pn]
                filter_desc.append(f"料号 = '{target_pn}'")
                
        # Filter by Period if specified
        if col_pd != "--不使用--":
            target_pd = self.val_period.get().strip()
            if target_pd:
                df_filtered = df_filtered[df_filtered[col_pd].astype(str) == target_pd]
                filter_desc.append(f"周期 = '{target_pd}'")
                
        # Check if data is empty after filtering
        if len(df_filtered) == 0:
            self.log_result(f"筛选条件: {', '.join(filter_desc) if filter_desc else '无'}\n未找到匹配的数据！")
            return
            
        # Calculate Metrics
        try:
            # Ensure the columns are numeric
            total_qty = pd.to_numeric(df_filtered[col_tot], errors='coerce').sum()
            pass_qty = pd.to_numeric(df_filtered[col_pas], errors='coerce').sum()
            
            # Count lots (number of rows after filtering)
            total_lots = len(df_filtered)
            
            # Simple assumption for LAR calculation: 
            # A lot is 'accepted' if pass_qty == total_qty (or based on some logic)
            # Here, we'll calculate Yield (total pass / total qty)
            # And for LAR, we'll assume a lot is accepted if its individual yield > 0
            # You might need to adjust this logic based on your specific LAR definition
            
            # Calculate individual yields to determine accepted lots
            df_filtered['yield'] = pd.to_numeric(df_filtered[col_pas], errors='coerce') / pd.to_numeric(df_filtered[col_tot], errors='coerce')
            
            # Let's assume a lot is accepted if its yield is 100% (or adjust threshold as needed)
            # You can change >= 0.99 to whatever your quality standard is
            accepted_lots = len(df_filtered[df_filtered['yield'] >= 0.98]) # Assuming >=98% is passing for a lot
            
            # Yield Calculation
            overall_yield = (pass_qty / total_qty) * 100 if total_qty > 0 else 0
            
            # LAR Calculation
            lar = (accepted_lots / total_lots) * 100 if total_lots > 0 else 0
            
            # Prepare result message
            res_msg = "=== 计算完成 ===\n"
            if filter_desc:
                res_msg += f"筛选条件: {', '.join(filter_desc)}\n"
            else:
                res_msg += "筛选条件: 无 (全表数据)\n"
                
            res_msg += f"匹配行数 (批次): {total_lots}\n"
            res_msg += "-" * 20 + "\n"
            res_msg += f"总投入量: {total_qty:,.2f}\n"
            res_msg += f"总合格量: {pass_qty:,.2f}\n"
            res_msg += f"综合良率 (Yield): {overall_yield:.2f}%\n"
            res_msg += f"批次接收率 (LAR): {lar:.2f}% (按单批良率>=98%计算)\n"
            
            self.log_result(res_msg)
            
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中发生错误:\n请确保所选的计算列包含有效的数值。\n错误信息: {str(e)}")

    def log_result(self, message):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    try:
        style.theme_use('clam') # Use a slightly more modern theme if available
    except:
        pass
        
    app = DataAnalyzerApp(root)
    root.mainloop()
