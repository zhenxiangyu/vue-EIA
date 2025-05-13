import math
import tkinter as tk
from tkinter import ttk, messagebox
import folium
from folium.plugins import Draw
import io
import requests
from PIL import Image, ImageTk
import pyproj

class NoisePredictionGIS:
    def __init__(self, root):
        self.root = root
        self.root.title("工业噪声预测GIS系统")
        self.map_frame = None
        self.current_markers = []
        self.setup_ui()
        
        # 坐标转换器（WGS84转UTM）
        self.transformer = pyproj.Transformer.from_crs(4326, 32650, always_xy=True)  # 示例使用UTM 50N

    def setup_ui(self):
        # 主容器
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # 左侧控制面板
        control_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(control_frame)

        # 右侧地图面板
        self.map_frame = ttk.Frame(main_paned)
        main_paned.add(self.map_frame)

        # 控制面板内容
        self.setup_control_panel(control_frame)
        self.init_map(31.2304, 121.4737)  # 初始定位上海

    def setup_control_panel(self, parent):
        # 地图操作区
        map_ctrl_frame = ttk.LabelFrame(parent, text="地图操作")
        map_ctrl_frame.pack(padx=10, pady=5, fill=tk.X)

        ttk.Button(map_ctrl_frame, text="添加厂房", command=lambda: self.set_draw_mode('rectangle')).pack(side=tk.LEFT)
        ttk.Button(map_ctrl_frame, text="添加噪声源", command=lambda: self.set_draw_mode('marker')).pack(side=tk.LEFT)
        ttk.Button(map_ctrl_frame, text="清除标注", command=self.clear_markers).pack(side=tk.LEFT)

        # 预测参数区
        param_frame = ttk.LabelFrame(parent, text="预测参数")
        param_frame.pack(padx=10, pady=5, fill=tk.X)

        ttk.Label(param_frame, text="背景噪声(dB):").grid(row=0, column=0)
        self.background_entry = ttk.Entry(param_frame)
        self.background_entry.grid(row=0, column=1)
        self.background_entry.insert(0, "45")

        # 结果展示
        self.result_label = ttk.Label(parent, text="预测结果：等待计算...", font=('Arial', 12))
        self.result_label.pack(pady=10)

    def init_map(self, lat, lon):
        """初始化Folium地图"""
        self.map = folium.Map(
            location=[lat, lon],
            zoom_start=16,
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery'
        )
        Draw(export=True).add_to(self.map)
        self.update_map_display()

    def update_map_display(self):
        """更新地图显示"""
        img_data = self.map._to_png()
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((800, 600), Image.Resampling.LANCZOS)
        self.tkimage = ImageTk.PhotoImage(img)
        
        if hasattr(self, 'map_label'):
            self.map_label.config(image=self.tkimage)
        else:
            self.map_label = ttk.Label(self.map_frame, image=self.tkimage)
            self.map_label.pack()

    def set_draw_mode(self, mode):
        """设置地图绘制模式"""
        self.map.add_child(folium.LatLngPopup())
        self.root.after(100, lambda: self.handle_draw(mode))

    def handle_draw(self, mode):
        """处理地图绘制事件"""
        if mode == 'marker':
            def add_source(e):
                popup = folium.Popup(self.get_marker_form(e.latlng))
                folium.Marker(
                    location=e.latlng,
                    popup=popup,
                    icon=folium.Icon(color='red')
                ).add_to(self.map)
                self.update_map_display()
            
            self.map.add_child(folium.ClickForMarker(popup=add_source))

        elif mode == 'rectangle':
            def add_factory(bounds):
                popup = folium.Popup(self.get_factory_form(bounds))
                folium.Rectangle(
                    bounds=bounds,
                    popup=popup,
                    color='#3186cc',
                    fill=True
                ).add_to(self.map)
                self.update_map_display()
            
            self.map.add_child(folium.ClickForMarker(popup=add_factory))

    def get_marker_form(self, latlng):
        """噪声源参数输入表单"""
        form_html = f"""
        <div style="width: 200px;">
            <h4>噪声源参数</h4>
            <label>声功率级(dB):</label>
            <input type="number" id="lw" value="100"><br>
            <label>类型:</label>
            <select id="type">
                <option value="outdoor">室外声源</option>
                <option value="indoor">室内声源</option>
            </select><br>
            <button onclick="saveData()">保存</button>
        </div>
        <script>
            function saveData(){{
                let data = {{
                    'lat': {latlng[0]},
                    'lon': {latlng[1]},
                    'lw': document.getElementById('lw').value,
                    'type': document.getElementById('type').value
                }};
                window.parent.postMessage(data, '*');
            }}
        </script>
        """
        return form_html

    def get_factory_form(self, bounds):
        """厂房参数输入表单"""
        form_html = f"""
        <div style="width: 250px;">
            <h4>厂房参数</h4>
            <label>厂房名称:</label>
            <input type="text" id="name"><br>
            <label>隔声量(dB):</label>
            <input type="number" id="tl" value="30"><br>
            <button onclick="saveData()">保存</button>
        </div>
        <script>
            function saveData(){{
                let data = {{
                    'bounds': {bounds},
                    'name': document.getElementById('name').value,
                    'tl': document.getElementById('tl').value
                }};
                window.parent.postMessage(data, '*');
            }}
        </script>
        """
        return form_html

    def clear_markers(self):
        """清除所有标注"""
        for marker in self.current_markers:
            self.map.remove_layer(marker)
        self.update_map_display()

    def wgs84_to_utm(self, lon, lat):
        """坐标转换：WGS84转UTM"""
        x, y = self.transformer.transform(lon, lat)
        return x, y

    def calculate_noise(self):
        """执行噪声预测计算"""
        try:
            # 获取所有噪声源
            sources = []
            for layer in self.map._children.values():
                if isinstance(layer, folium.Marker):
                    x, y = self.wgs84_to_utm(layer.location[1], layer.location[0])
                    sources.append({
                        'type': layer.options.get('type', 'outdoor'),
                        'Lw': float(layer.options.get('lw', 100)),
                        'pos': (x, y, 0)
                    })

            # 执行预测计算（示例简化）
            total = 10 * math.log10(sum(10**(s['Lw']/10) for s in sources))
            background = float(self.background_entry.get())
            total = 10 * math.log10(10**(total/10) + 10**(background/10))
            
            self.result_label.config(
                text=f"预测噪声值：{total:.1f} dB(A)",
                foreground="green"
            )
            
        except Exception as e:
            messagebox.showerror("计算错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = NoisePredictionGIS(root)
    root.geometry("1200x800")
    root.mainloop()