import json
import os
import sys
import time

def slow_print(text, delay=0.02):
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class Player:
    def __init__(self):
        self.humanity = 50      
        self.knowledge = 10      
        self.tsypa_trust = 50    
        self.motya_alive = True  
        self.current_scene = "prologue"

    def apply_effects(self, effects):
        if not effects:
            return
        self.humanity = max(0, min(100, self.humanity + effects.get("humanity", 0)))
        self.knowledge = max(0, min(100, self.knowledge + effects.get("knowledge", 0)))
        self.tsypa_trust = max(0, min(100, self.tsypa_trust + effects.get("tsypa_trust", 0)))
        
        if "motya_alive" in effects:
            self.motya_alive = effects["motya_alive"]

    def show_stats(self):
        print("\n" + "="*40)
        print(" ТВОИ ХАРАКТЕРИСТИКИ:")
        print(f" Человечность:   [{self.humanity}/100]")
        print(f" Осведомленность:[{self.knowledge}/100]")
        print(f" Доверие Цыпы:   [{self.tsypa_trust}/100]")
        print(f" Статус Моти:    {'Жив' if self.motya_alive else 'Мертв'}")
        print("="*40 + "\n")

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)


class Choice:
    def __init__(self, text, next_scene_id, effects=None):
        self.text = text
        self.next_scene_id = next_scene_id
        self.effects = effects or {}


class Scene:
    def __init__(self, title, description, choices):
        self.title = title
        self.description = description
        self.choices = choices


class Game:
    def __init__(self):
        self.player = Player()
        self.scenes = {}
        self.save_file = "savegame.json" 
        self.setup_scenes()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def save_game(self):
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(self.player.to_dict(), f, ensure_ascii=False, indent=4)
        slow_print("\n[!] Игра успешно сохранена!", 0.01)

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.player.from_dict(data)
            slow_print("\n[!] Игра загружена", 0.01)
        else:
            slow_print("\n[!] Файл сохранения не найден.", 0.01)

    def setup_scenes(self):
        
        self.scenes["prologue"] = Scene(
            "Пролог: Смерть на Литейном",
            "Санкт-Петербург, 1994 год. Зимний вечер.\n\n"
            "Вы — Александр Яковлев, 16 лет. Машина вашей семьи взорвана.\n"
            "Вы теряете сознание на снегу, левая сторона тела горит. Осколок выбивает левый глаз.\n"
            "Голос сквозь шум: «Всё чисто, заказывай машину. Егерия не прощает должников».\n\n"
            "Вы выжили. Три года спустя вы поклялись отомстить группировке «Егерия».\n"
            "Ваше тело покрыто шрамами и бинтами, левый глаз скрыт повязкой.\n"
            "Вы тренировались, и теперь пришло время действовать.",
            [
                Choice("Начать месть", "act1")
            ]
        )

        self.scenes["act1"] = Scene(
            "Акт 1. Тень на Малой Садовой",
            "Подвал на Малой Садовой. Ваши союзники: Мотя (старый друг), Цыпа (дерзкая девушка) и Хирург (бывший военврач).\n"
            "Информатор Косой сообщает: «Егерией» руководит Егерь. Его правая рука — Мамонт.\n"
            "Вам нужно решить, как действовать дальше.",
            [
                Choice("Кровавый след – убить Мамонта. Быстро, громко, но Егерь уйдёт в подполье.", "act2_blood", 
                       {"humanity": -15, "knowledge": 5}),
                Choice("Паутина – следить за Мамонтом, найти слабое место, узнать правду.", "act2_web", 
                       {"humanity": 5, "knowledge": 25, "tsypa_trust": 10}),
                Choice("Тихий сбор – похитить дочь полевого командира Бородая, выбить информацию.", "act2_silent", 
                       {"humanity": -30, "knowledge": 15})
            ]
        )

        self.scenes["act2_blood"] = Scene(
            "Акт 2. Зимняя охота (Кровавый след)",
            "Косой передаёт записку: «Выходи на стрелку в промзону Парнаса. Егерь хочет договориться. Один».\n"
            "Это явная ловушка. Что вы предпримете?",
            [
                Choice("Взять с собой Мотю и Цыпу в засаду", "act3_finale", 
                       {"tsypa_trust": 15, "humanity": 5}),
                Choice("Пойти одному, но с гранатой (Риск)", "act3_finale", 
                       {"humanity": -10, "tsypa_trust": -10})
            ]
        )

        self.scenes["act2_web"] = Scene(
            "АКТ 2: ПАУТИНА",
            "Вы выяснили, что Мамонт ворует у Егеря. У вас есть компромат.\n"
            "Вы сидите перед Мамонтом в сауне, разматывая бинты на руке.",
            [
                Choice("Перевербовать: Пусть даст показания против Егеря", "act3_justice", 
                       {"humanity": 20, "knowledge": 20}),
                Choice("Стравить: Подбросить инфу Егерю, пусть сами перебьют друг друга", "act3_finale", 
                       {"humanity": -10})
            ]
        )

        self.scenes["act2_silent"] = Scene(
            "АКТ 2: ТИХИЙ СБОР",
            "Девочка сидит в запертой квартире. Бородай готов дать имена убийц семьи в обмен на дочь.\n"
            "Галлюцинация: На месте девочки вы видите свою погибшую сестру.",
            [
                Choice("Обменять девочку на имена палачей и убить их всех.", "act3_finale", 
                       {"humanity": -40, "tsypa_trust": -20}),
                Choice("Отпустить девочку: «Скажи отцу, Яковлев вернул долг чести».", "act3_finale", 
                       {"humanity": 30, "tsypa_trust": 25})
            ]
        )

        self.scenes["act3_finale"] = Scene(
            "АКТ 3: ЛОГОВО ЕГЕРЯ",
            "Особняк на Каменном острове. Егерь окружен охраной.\n"
            "Егерь: «Твой отец предал нас. Вы оба гнилые...»\n"
            "Голос отца в голове: «Убей их всех, Саша. Выжги дотла».",
            [
                Choice("Быстрая смерть: Застрелить Егеря (Концовка: Волчья стая)", "ending_wolf", 
                       {"humanity": -10}),
                Choice("Око за око: Выколоть ему глаз и сжечь заживо (Концовка: Монстр)", "ending_monster", 
                       {"humanity": -50})
            ]
        )

        self.scenes["act3_justice"] = Scene(
            "АКТ 3: ПРАВОСУДИЕ",
            "Хирург привел группу захвата. Егерь связан и кричит угрозы.",
            [
                Choice("Передать Егеря ментам (Концовка: Феникс)", "ending_phoenix", 
                       {"humanity": 20})
            ]
        )

        self.scenes["ending_wolf"] = Scene(
            "КОНЦОВКА: ВОЛЧЬЯ СТАЯ",
            "Вы выходите из горящего особняка. Цыпа рядом.\n"
            "Саша: «Теперь я должен стать тем, кого они боятся». Вы продолжаете войну.\n"
            "*** ИГРА ОКОНЧЕНА ***", []
        )
        self.scenes["ending_monster"] = Scene(
            "КОНЦОВКА: МОНСТР",
            "Вы стали авторитетом. Бинты сменили на черную форму. Цыпа смотрит на вас с холодом. Мотя ушел.\n"
            "Вы улыбаетесь невидимому отцу. Вы стали хуже Егеря.\n"
            "*** ИГРА ОКОНЧЕНА ***", []
        )
        self.scenes["ending_phoenix"] = Scene(
            "КОНЦОВКА: ФЕНИКС",
            "Егерь сидит пожизненно. Вы снимаете повязку перед зеркалом.\n"
            "Вы в кафе с Цыпой и Мотей. Вы пытаетесь жить как люди.\n"
            "*** ИГРА ОКОНЧЕНА ***", []
        )

    def play(self):
        while True:
            self.clear_screen()

            scene = self.scenes[self.player.current_scene]
            
    
            slow_print(f"=== {scene.title} ===\n", delay=0.03)
            slow_print(scene.description, delay=0.02)
            print("\n" + "-"*40)

            if not scene.choices:
                print("\nНажмите Enter, чтобы выйти...")
                input()
                break

            print("Ваши действия:")
            
            for i, choice in enumerate(scene.choices, 1):
                print(f" {i}. {choice.text}")

            print("\n[Х] - Характеристики | [С] - Сохранить | [З] - Загрузить | [В] - Выход")
            
            answer = input("Ваш выбор: ").strip().lower()

            if answer == 'х':
                self.player.show_stats()
                input("Нажмите Enter, чтобы продолжить...")
                continue
            elif answer == 'с':
                self.save_game()
                input("Нажмите Enter, чтобы продолжить...")
                continue
            elif answer == 'з':
                self.load_game()
                input("Нажмите Enter, чтобы продолжить...")
                continue
            elif answer == 'в':
                slow_print("Выход из игры...", 0.03)
                break

            try:
                choice_index = int(answer) - 1
                if 0 <= choice_index < len(scene.choices):
                    selected_choice = scene.choices[choice_index]
                    self.player.apply_effects(selected_choice.effects)
                    self.player.current_scene = selected_choice.next_scene_id
                else:
                    print("Неверный номер. Попробуйте снова.")
                    input()
            except ValueError:
                print("Пожалуйста, введите номер действия или букву из меню.")
                input()


if __name__ == "__main__":
    game = Game()
    game.play()

   