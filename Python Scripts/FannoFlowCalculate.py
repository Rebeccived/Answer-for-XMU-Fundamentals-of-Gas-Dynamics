# -*- coding: utf-8 -*-
"""
Fanno 流比值计算程序
使用数字选择比值，输出显示 Unicode 下标
"""

import numpy as np
from scipy.optimize import fsolve

# -------------------- Fanno 流函数 --------------------
def fanno_ratios(M, gamma=1.4):
    """
    已知马赫数 M，计算 Fanno 流各比值
    返回字典，显示 Unicode 下标
    """
    ratios = {}
    ratios['T/T*'] = (gamma+1)/2 / (1 + (gamma-1)/2 * M**2)
    ratios['p/p*'] = 1/M * ((gamma+1)/2 / (1 + (gamma-1)/2 * M**2))**0.5
    ratios['pₜ/pₜ*'] = 1/M * ((1 + (gamma-1)/2 * M**2)/((gamma+1)/2))**((gamma+1)/(2*(gamma-1)))
    ratios['fL/D'] = (gamma+1)/(2*gamma) * np.log(((gamma+1)/2 * M**2)/(1 + (gamma-1)/2 * M**2)) + 1/gamma * (1/M**2 - 1)
    ratios['Sₘₐₓ/R'] = np.log(1/M * ((1 + (gamma-1)/2 * M**2)/(1 + (gamma-1)/2))**((gamma+1)/(2*(gamma-1))))
    ratios['V/V*'] = M * np.sqrt((gamma+1)/(2 + (gamma-1)*M**2))
    return ratios

# -------------------- 反求马赫数 --------------------
def solve_M_from_ratio(value, ratio_key, gamma=1.4, supersonic=True):
    func = lambda M: fanno_ratios(M, gamma)[ratio_key] - value
    M0 = 2.0 if supersonic else 0.3
    M_solution, = fsolve(func, M0)
    return M_solution

# -------------------- 主程序 --------------------
if __name__ == "__main__":
    ratio_dict = {
        "1": "T/T*",
        "2": "p/p*",
        "3": "pₜ/pₜ*",
        "4": "fLₘₐₓ/D",
        "5": "Sₘₐₓ/R",
        "6": "V/V*"
    }

    print("Fanno 流比值计算程序\n")
    print("模式选择：")
    print("1 = 已知 M 求其余比值")
    print("2 = 已知比值求 M 并输出其他比值")
    mode = input("请输入模式编号 (1/2)：").strip()

    gamma = input("请输入比热比 γ（默认 1.4，可直接回车）：").strip()
    gamma = float(gamma) if gamma else 1.4

    if mode == "1":
        M = float(input("请输入马赫数 M："))
        ratios = fanno_ratios(M, gamma)
        print(f"\n已知 M={M:.6f}，计算比值如下：")
        for k, v in ratios.items():
            print(f"{k} = {v:.6f}")

    elif mode == "2":
        print("可选择的比值：")
        for num, name in ratio_dict.items():
            print(f"{num} = {name}")
        choice = input("请输入数字选择比值：").strip()
        ratio_name = ratio_dict.get(choice)
        if ratio_name is None:
            print("输入数字错误！")
        else:
            value = float(input(f"请输入 {ratio_name} 的值："))
            branch = input("求解分支：1 = 亚音速；2 = 超音速：")
            supersonic = (branch == "2")
            M = solve_M_from_ratio(value, ratio_name, gamma, supersonic)
            print(f"\n求得马赫数 M = {M:.6f}")
            ratios = fanno_ratios(M, gamma)
            print("对应的其他比值：")
            for k, v in ratios.items():
                if k != ratio_name:
                    print(f"{k} = {v:.6f}")
    else:
        print("模式输入错误，请输入 1 或 2。")
