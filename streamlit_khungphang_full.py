
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians, degrees, sqrt
from sympy import symbols, Eq, solve, sympify, simplify

st.set_page_config(layout="wide")
st.title("Mô phỏng Hệ Khung Phẳng")

st.sidebar.header("Thông số Vật liệu và Hình học")

E = float(st.sidebar.text_input("E (N/m²)", "2e11"))
v = float(st.sidebar.text_input("v", "0.3"))
A = float(st.sidebar.text_input("A (m²)", "0.01"))
I = float(st.sidebar.text_input("I (m⁴)", "0.00001"))

st.sidebar.markdown("---")

num_nodes = st.sidebar.number_input("Số lượng Node", min_value=2, step=1)
num_elements = st.sidebar.number_input("Số lượng phần tử", min_value=1, step=1)

coords = []
elements = []

st.subheader("Tọa độ các Node (x, y)")

for i in range(int(num_nodes)):
    col1, col2 = st.columns(2)
    x = col1.number_input(f"x{i+1}", key=f"x{i}", value=0.0)
    y = col2.number_input(f"y{i+1}", key=f"y{i}", value=0.0)
    coords.append((x, y))

st.subheader("Danh sách phần tử (i, j)")

for i in range(int(num_elements)):
    col1, col2 = st.columns(2)
    ni = col1.number_input(f"Node i - phần tử {i+1}", min_value=1, max_value=int(num_nodes), key=f"e{i}_start")
    nj = col2.number_input(f"Node j - phần tử {i+1}", min_value=1, max_value=int(num_nodes), key=f"e{i}_end")
    elements.append((int(ni)-1, int(nj)-1))

# Vẽ sơ đồ khung
if st.button("Vẽ sơ đồ khung"):
    fig, ax = plt.subplots()
    for i, (start, end) in enumerate(elements):
        x1, y1 = coords[start]
        x2, y2 = coords[end]
        ax.plot([x1, x2], [y1, y2], 'bo-', label=f"Phần tử {i+1}")
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{i+1}", color="red")

    for i, (x, y) in enumerate(coords):
        ax.text(x, y, f"{i+1}", fontsize=10, color="green")

    ax.set_aspect("equal")
    ax.set_title("Sơ đồ Hệ Khung")
    st.pyplot(fig)

# Tính toán Ke
if st.button("Tính ma trận độ cứng phần tử Ke"):
    st.subheader("Ma trận độ cứng phần tử Ke")
    Ke_all = []
    for idx, (i, j) in enumerate(elements):
        xi, yi = coords[i]
        xj, yj = coords[j]
        L = sqrt((xj - xi)**2 + (yj - yi)**2)
        angle = radians(degrees(np.arctan2((yj - yi), (xj - xi))))
        c = cos(angle)
        s = sin(angle)
        B = (12 * I) / (L ** 2)
        a11 = ((A * c**2 + B * s**2) / L)
        a22 = ((A * s**2 + B * c**2) / L)
        a33 = (4 * I / L)
        a12 = ((A - B) * c * s / L)
        a13 = (-(B * L * s) / 2 / L)
        a23 = ((B * L * c) / 2 / L)
        a36 = (2 * I / L)
        Ke = np.array([
            [a11, a12, a13, -a11, -a12, a13],
            [a12, a22, a23, -a12, -a22, a23],
            [a13, a23, a33, -a13, -a23, a36],
            [-a11, -a12, -a13, a11, a12, -a13],
            [-a12, -a22, -a23, a12, a22, -a23],
            [a13, a23, a36, -a13, -a23, a33]
        ])
        Ke = np.round(Ke, 5)
        Ke_all.append(Ke)
        st.markdown(f"**Phần tử {idx+1}** (L={L:.3f}):")
        st.text(Ke)

# Tiếp theo (ở lần cập nhật sau): Tính K tổng thể, Pe, P, q, phản lực
