def hash_round(team1_letters, team2_letters, round_number):
    team1_value = sum(ord(char) - ord('A') + 1 for char in team1_letters)
    team2_value = sum(ord(char) - ord('A') + 1 for char in team2_letters)
    hash_result = ((team1_value * 31) ^ (team2_value * 17) + round_number) % 31
    if hash_result == 0:
        hash_result = 31
    return hash_result

equivalents_arabic = {
    1: "🏆 فوز الفريق 1",
    2: "🤝 تعادل في المباراة",
    3: "🏅 فوز الفريق 2",
    4: "⚽ الفريق 1 يفوز أو يتعادل",
    5: "🔄 فوز الفريق 1 أو الفريق 2",
    6: "🔄 الفريق 2 يفوز أو يتعادل",
    7: "📈 الفريق 1 يسجل أكثر من هدف",
    8: "⚽ فوز الفريق 1 أو 2 بفرق هدف واحد",
    9: "📈 الفريق 2 يسجل أكثر من هدف",
    10: "⚽ الفريق 1 يربح أو يتعادل",
    11: "⚽ الفريق 1 و 2 يسجل في المباراة",
    12: "📈 الفريق 2 يسجل أكثر من هدف",
    13: "🔻 أقل من هدفين في المباراة",
    14: "🔺 أكثر من هدفين في المباراة",
    15: "🔻 أقل من 3 أهداف في المباراة",
    16: "🔺 أكثر من 2.5 هدف",
    17: "🔻 أقل من 3.5 هدف",
    18: "🔺 أكثر من 3.5 هدف",
    19: "🔻 أقل من هدفين في الشوط الأول أو الثاني",
    20: "🔺 أكثر من هدفين في الشوط الأول أو الثاني",
    21: "⚽ الفريق 1 سيسجل في المباراة",
    22: "🤝 تعادل في المباراة",
    23: "⚽ الفريق 2 سيسجل في المباراة",
    24: "🔄 فوز الفريق 1 أو أقل من 2.5 هدف",
    25: "🤝 تعادل في المباراة أو أقل من 2.5 هدف",
    26: "📈 الفريق 1 سيسجل أكثر من 1.5 هدف",
    27: "🔄 فوز الفريق 2 أو أقل من 2.5 هدف",
    28: "🔺 أكثر من 3.5 هدف في المباراة",
    29: "📈 الفريق 2 سيسجل أكثر من 1.5 هدف",
    30: "⚽ الفريق 1 و 2 سيسجلان في المباراة",
    31: "🚫 لن يسجل كلا الفريقين 1 و 2"
}

def predict_match_result(team1_goals, team2_goals):
    if team1_goals > team2_goals:
        return "🏆 الفريق 1 يفوز"
    elif team2_goals > team1_goals:
        return "🏅 الفريق 2 يفوز"
    else:
        return "🤝 تعادل"

def get_last_3_matches_results(team_name):
    results = []
    goals = []
    print(f"🔄 أدخل نتائج آخر 3 مباريات للفريق {team_name}:")
    for i in range(1, 4):
        result = input(f"نتيجة المباراة {i} (فوز/خسارة/تعادل): ").strip()
        goal = int(input(f"عدد الأهداف المسجلة في المباراة {i}: "))
        results.append(result)
        goals.append(goal)
    return results, goals

def calculate_potential_goals(team1_goals_list, team2_goals_list):
    team1_avg_goals = sum(team1_goals_list) / len(team1_goals_list)
    team2_avg_goals = sum(team2_goals_list) / len(team2_goals_list)
    total_potential_goals = (team1_avg_goals + team2_avg_goals) / 2
    return total_potential_goals

def calculate_goal_probabilities(goals_list):
    probabilities = {}
    thresholds = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    
    for threshold in thresholds:
        count = sum(1 for goals in goals_list if goals > threshold)
        probabilities[f"أكثر من {threshold} هدف"] = (count / len(goals_list)) * 100
        probabilities[f"أقل من {threshold} هدف"] = ((len(goals_list) - count) / len(goals_list)) * 100
    
    return probabilities

def calculate_both_teams_to_score_probability(team1_goals_list, team2_goals_list):
    both_teams_to_score = sum(1 for g1, g2 in zip(team1_goals_list, team2_goals_list) if g1 > 0 and g2 > 0)
    return (both_teams_to_score / len(team1_goals_list)) * 100

def calculate_win_or_draw_probabilities(results_list):
    win_count = results_list.count("فوز")
    draw_count = results_list.count("تعادل")
    return {
        "الفوز": (win_count / len(results_list)) * 100,
        "التعادل": (draw_count / len(results_list)) * 100
    }

# إدخال البيانات
print("🔍 أداة تحليل المباريات - صنع من طرف BET FLEX 🔍".center(50, '='))
team1_letters = input("🔠 أدخل الأحرف الثلاثة للفريق 1: ").upper()
team2_letters = input("🔠 أدخل الأحرف الثلاثة للفريق 2: ").upper()
team1_goals = int(input("⚽ أدخل عدد أهداف الفريق 1: "))
team2_goals = int(input("⚽ أدخل عدد أهداف الفريق 2: "))
round_number = int(input("🔢 أدخل رقم الجولة: "))

# الحصول على نتائج آخر 3 مباريات
team1_last_3_matches, team1_last_3_goals = get_last_3_matches_results(team1_letters)
team2_last_3_matches, team2_last_3_goals = get_last_3_matches_results(team2_letters)

# التحقق من أن رقم الجولة بين 1 و31
if 1 <= round_number <= 31:
    hash_result = hash_round(team1_letters, team2_letters, round_number)
    result = equivalents_arabic.get(hash_result, "❓ نتيجة غير معروفة")
    predicted_result = predict_match_result(team1_goals, team2_goals)
    
    # حساب عدد الأهداف المحتملة
    potential_goals = calculate_potential_goals(team1_last_3_goals, team2_last_3_goals)
    
    # حساب نسب مئوية للأهداف المحتملة
    team1_probabilities = calculate_goal_probabilities(team1_last_3_goals)
    team2_probabilities = calculate_goal_probabilities(team2_last_3_goals)
    
    # حساب احتمال تسجيل كلا الفريقين
    both_teams_to_score_probability = calculate_both_teams_to_score_probability(team1_last_3_goals, team2_last_3_goals)
    
    # حساب نسب مئوية للفوز أو التعادل
    team1_win_draw_probabilities = calculate_win_or_draw_probabilities(team1_last_3_matches)
    team2_win_draw_probabilities = calculate_win_or_draw_probabilities(team2_last_3_matches)
    
    # عرض التفاصيل
    print("\n📋 تفاصيل المباراة:")
    print(f"🏆 الفريق 1: {team1_letters} - عدد الأهداف: {team1_goals}")
    print(f"🏆 الفريق 2: {team2_letters} - عدد الأهداف: {team2_goals}")
    print(f"🔢 رقم الجولة: {round_number}")
    print("\n📝 نتيجة المباراة هي:".center(50))
    print(result.center(50))
    print("\n🔮 التوقع المحتمل لنتيجة المباراة:".center(50))
    print(predicted_result.center(50))
    print(f"\n⚽ عدد الأهداف المحتملة في المباراة: {potential_goals:.2f}".center(50))
    
    # عرض نتائج آخر 3 مباريات لكل فريق
    print("\n📊 آخر 3 نتائج للفريق 1:")
    for idx, res in enumerate(team1_last_3_matches, 1):
        print(f"مباراة {idx}: {res} - عدد الأهداف: {team1_last_3_goals[idx-1]}")
    
    print("\n📊 آخر 3 نتائج للفريق 2:")
    for idx, res in enumerate(team2_last_3_matches, 1):
        print(f"مباراة {idx}: {res} - عدد الأهداف: {team2_last_3_goals[idx-1]}")
    
        # عرض احتمالات الأهداف للفريق 1
    print("\n📈 نسب مئوية لاحتمالات تسجيل الفريق 1:")
    for key, value in team1_probabilities.items():
        print(f"{key}: {value:.2f}%")
    
    # عرض احتمالات الأهداف للفريق 2
    print("\n📈 نسب مئوية لاحتمالات تسجيل الفريق 2:")
    for key, value in team2_probabilities.items():
        print(f"{key}: {value:.2f}%")
    
    # عرض احتمالات عدم تسجيل أهداف للفريق 1
    print("\n🚫 نسب مئوية لعدم تسجيل الفريق 1:")
    for threshold in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
        below_threshold = 100 - team1_probabilities[f"أكثر من {threshold} هدف"]
        print(f"أقل من {threshold} هدف: {below_threshold:.2f}%")
    
    # عرض احتمالات عدم تسجيل أهداف للفريق 2
    print("\n🚫 نسب مئوية لعدم تسجيل الفريق 2:")
    for threshold in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
        below_threshold = 100 - team2_probabilities[f"أكثر من {threshold} هدف"]
        print(f"أقل من {threshold} هدف: {below_threshold:.2f}%")
    
    # عرض احتمالات تسجيل كلا الفريقين
    print(f"\n⚽ احتمال تسجيل كلا الفريقين في المباراة: {both_teams_to_score_probability:.2f}%")
    
    # عرض احتمالات الفوز أو التعادل للفريق 1
    print("\n🔍 نسب مئوية للفوز أو التعادل للفريق 1:")
    for key, value in team1_win_draw_probabilities.items():
        print(f"{key}: {value:.2f}%")
    
    # عرض احتمالات الفوز أو التعادل للفريق 2
    print("\n🔍 نسب مئوية للفوز أو التعادل للفريق 2:")
    for key, value in team2_win_draw_probabilities.items():
        print(f"{key}: {value:.2f}%")

else:
    print("❗ يجب أن يكون رقم الجولة بين 1 و31.")

print("\n--- 🌟 شكراً لاستخدام أداة تحليل المباريات 🌟 ---".center(50))
print("🔧 صنع من طرف BET FLEX 🔧".center(50))
