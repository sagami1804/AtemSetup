import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox

def load_xml():
    """XMLファイルを読み込んでGUIに表示"""
    global tree, root, inputs_frame
    input_file = filedialog.askopenfilename(
        title="入力XMLファイルを選択してください",
        filetypes=[("XMLファイル", "*.xml")]
    )
    if not input_file:
        return

    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
        inputs = root.find(".//Inputs")
        if inputs is None:
            messagebox.showerror("エラー", "Inputsセクションが見つかりませんでした。")
            return

        # 既存のウィジェットをクリア
        for widget in inputs_frame.winfo_children():
            widget.destroy()

        # 各Inputの情報を表示
        for input_elem in inputs.findall("Input"):
            input_id = input_elem.get("id")
            current_long_name = input_elem.get("longName", "")
            tk.Label(inputs_frame, text=f"ID={input_id}").pack(anchor="w")
            entry = tk.Entry(inputs_frame, width=40)
            entry.insert(0, current_long_name)
            entry.pack(anchor="w")
            entry_map[input_id] = (input_elem, entry)

    except Exception as e:
        messagebox.showerror("エラー", f"XMLファイルの読み込み中にエラーが発生しました: {e}")

def save_xml():
    """編集されたlongNameをXMLに反映して保存"""
    if not tree or not root:
        messagebox.showerror("エラー", "XMLファイルが読み込まれていません。")
        return

    # 各エントリの値をXMLに反映
    for input_id, (input_elem, entry) in entry_map.items():
        new_long_name = entry.get()
        input_elem.set("longName", new_long_name)

    # 保存先を選択
    output_file = filedialog.asksaveasfilename(
        title="出力XMLファイルを保存する場所を選択してください",
        defaultextension=".xml",
        filetypes=[("XMLファイル", "*.xml")]
    )
    if not output_file:
        return

    try:
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("完了", f"新しいXMLファイルが {output_file} に保存されました。")
    except Exception as e:
        messagebox.showerror("エラー", f"XMLファイルの保存中にエラーが発生しました: {e}")

# メインウィンドウの作成
root_window = tk.Tk()
root_window.title("ATEM Setting Mapper")

# フレームの作成
inputs_frame = tk.Frame(root_window)
inputs_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ボタンの作成
button_frame = tk.Frame(root_window)
button_frame.pack(fill="x", padx=10, pady=10)

load_button = tk.Button(button_frame, text="XMLを読み込む", command=load_xml)
load_button.pack(side="left", padx=5)

save_button = tk.Button(button_frame, text="XMLを保存する", command=save_xml)
save_button.pack(side="right", padx=5)

# グローバル変数
tree = None
root = None
entry_map = {}

# メインループの開始
root_window.mainloop()