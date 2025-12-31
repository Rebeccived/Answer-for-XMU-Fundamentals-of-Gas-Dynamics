# -*- coding: utf-8 -*-
"""
马赫数 M 与比值互算程序
比值类型：
1 = A/A*
2 = T/Tₜ
3 = p/pₜ
4 = ρ/ρₜ
5 = pA/pₜA*
"""

import numpy as np
from scipy.optimize import fsolve

# --------------------------- 参数 ---------------------------
gamma_default = 1.4

# Unicode 下标 + 比值名称
ratio_dict = {
    '1': 'A/A*',
    '2': 'T/Tₜ',
    '3': 'p/pₜ',
    '4': 'ρ/ρₜ',
    '5': 'pA/pₜA*'
}

# --------------------------- 计算函数 ---------------------------
def mach_to_ratios(M, gamma=gamma_default):
    """通过马赫数计算五个比值"""

    # 面积比 A/A*
    A_Astar = 1/M * ((1 + (gamma-1)/2*M**2)/((gamma+1)/2))**((gamma+1)/(2*(gamma-1)))

    # 总温比 T/Tt
    T_Tt = 1 / (1 + (gamma-1)/2*M**2)

    # 总压比 p/pt
    p_pt = T_Tt**(gamma/(gamma-1))

    # 总密度比 ρ/ρt
    rho_rhot = T_Tt**(1/(gamma-1))

    # 新增：pA/pₜA*
    pA_p_tAstar = A_Astar * p_pt

    return A_Astar, T_Tt, p_pt, rho_rhot, pA_p_tAstar


def ratio_to_mach(value, ratio_type, gamma=gamma_default, supersonic=True):
    """已知比值求马赫数"""

    def func(M):
        A_Astar, T_Tt, p_pt, rho_rhot, pA_p_tAstar = mach_to_ratios(M, gamma)

        if ratio_type == '1':
            return A_Astar - value
        elif ratio_type == '2':
            return T_Tt - value
        elif ratio_type == '3':
            return p_pt - value
        elif ratio_type == '4':
            return rho_rhot - value
        elif ratio_type == '5':
            return pA_p_tAstar - value
        else:
            raise ValueError("比值类型必须是 1,2,3,4,5")

    # 初值选择（非常必要，防止跳分支）
    if ratio_type == '1':
        M0 = 0.5 if not supersonic else 2.0
    else:
        M0 = 0.5 if value > 1 else 2.0

    M_solution, = fsolve(func, M0)
    return M_solution


# --------------------------- 主程序 ---------------------------
if __name__ == "__main__":

    print("马赫数 M 与比值互算程序（共 5 种比值）\n")
    print("模式选择：")
    print("1 = 已知 M 求比值")
    print("2 = 已知比值求 M")
    mode = input("请输入模式编号 (1/2)：").strip()

    gamma = input("请输入比热比 γ（默认 1.4）：").strip()
    gamma = float(gamma) if gamma else gamma_default

    # ---------------------------------------------------------
    # 已知 M 求比值
    # ---------------------------------------------------------
    if mode == "1":
        M = float(input("请输入马赫数 M："))

        A_Astar, T_Tt, p_pt, rho_rhot, pA_p_tAstar = mach_to_ratios(M, gamma)

        print(f"\n马赫数 M = {M}\n")
        print(f"{ratio_dict['1']} = {A_Astar:.6f}")
        print(f"{ratio_dict['2']} = {T_Tt:.6f}")
        print(f"{ratio_dict['3']} = {p_pt:.6f}")
        print(f"{ratio_dict['4']} = {rho_rhot:.6f}")
        print(f"{ratio_dict['5']} = {pA_p_tAstar:.6f}")

    # ---------------------------------------------------------
    # 已知比值求 M
    # ---------------------------------------------------------
    elif mode == "2":
        print("可选比值类型：1=A/A*, 2=T/Tₜ, 3=p/pₜ, 4=ρ/ρₜ, 5=pA/pₜA*")
        ratio_type = input("请输入比值类型编号：").strip()

        ratio_value = float(input(f"请输入 {ratio_dict[ratio_type]} 的值："))

        supersonic = True
        if ratio_type == '1':
            branch = input("面积比 A/A* 反解分支：1=亚音速，2=超音速：").strip()
            supersonic = (branch == "2")

        M = ratio_to_mach(ratio_value, ratio_type, gamma, supersonic)

        A_Astar, T_Tt, p_pt, rho_rhot, pA_p_tAstar = mach_to_ratios(M, gamma)

        print(f"\n{ratio_dict[ratio_type]} = {ratio_value}  对应马赫数 M = {M:.6f}\n")
        print(f"{ratio_dict['1']} = {A_Astar:.6f}")
        print(f"{ratio_dict['2']} = {T_Tt:.6f}")
        print(f"{ratio_dict['3']} = {p_pt:.6f}")
        print(f"{ratio_dict['4']} = {rho_rhot:.6f}")
        print(f"{ratio_dict['5']} = {pA_p_tAstar:.6f}")

    else:
        print("模式输入错误，请输入 1 或 2。")
