import openpyxl

def write_to_merged(sheet, coordinate, value):
    """
    處理合併儲存格寫入的輔助函式。
    會自動尋找該座標所屬的合併區塊，並將資料寫入該區塊的「最左上角」。
    """
    for merged_range in sheet.merged_cells.ranges:
        if coordinate in merged_range:
            # 如果在這個合併區塊內，找出這個區塊的最左上角儲存格(min_row, min_col)來寫入
            sheet.cell(row=merged_range.min_row, column=merged_range.min_col).value = value
            return
            
    # 如果它不是合併儲存格，就照常直接寫入
    sheet[coordinate] = value

def generate_sample_report():
    # 請確認檔名與你資料夾內的範本檔名完全一致
    template_path = "HTWサービスリポート_希望Layout_(tsmc) - SAMPLE.xlsx"
    
    print("正在讀取 Excel 範本...")
    try:
        workbook = openpyxl.load_workbook(template_path)
        sheet = workbook.active
        
        print("正在寫入測試資料...")
        # 使用我們自訂的函式來寫入，完美避開唯讀錯誤！
        write_to_merged(sheet, 'H5', "竹科-F12P7")   # 寫入廠區
        write_to_merged(sheet, 'AN6', "APCD21")      # 寫入機台
        write_to_merged(sheet, 'G20', "Modify")      # 寫入作業
        
        output_path = "測試產出_維修服務報告書.xlsx"
        workbook.save(output_path)
        print(f"✅ 成功！已自動生成報表：{output_path}")
        
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    generate_sample_report()