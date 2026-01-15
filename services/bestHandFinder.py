from collections import Counter

class BestHandFinder: 


    def card_to_int(self, rank: int, suit: int) -> int:
        return rank * 10 + suit

    def get_rank(self, card: int) -> int:
        return card // 10

    def get_suit(self, card: int) -> int:
        return card % 10

    def evaluate_five_card_hand(self, hand: list[int]) -> tuple[int, list[int]]:
        ranks = [self.get_rank(card) for card in hand]
        suits = [self.get_suit(card) for card in hand]
        
        ranks_sorted = sorted(ranks, reverse=True)
        
        is_flush = len(set(suits)) == 1
        
        is_straight = False
        straight_high = 0
        
        unique_ranks = sorted(set(ranks), reverse=True)
        
        if set([14, 2, 3, 4, 5]).issubset(set(ranks)):
            is_straight = True
            straight_high = 5
            straight_ranks = [5, 4, 3, 2, 14]
        elif len(unique_ranks) == 5:
            for i in range(len(unique_ranks) - 4):
                window = unique_ranks[i:i+5]
                if window[0] - window[4] == 4:
                    is_straight = True
                    straight_high = window[0]
                    straight_ranks = window
                    break
        
        rank_counts = Counter(ranks)
        count_values = sorted(rank_counts.values(), reverse=True)
        most_common = rank_counts.most_common()
        
        if is_straight and is_flush:
            if straight_high == 14:
                return 9, [10]
            else:
                return 8, [straight_high]
        
        elif count_values[0] == 4:
            quad_rank = most_common[0][0]
            kicker = max([r for r in ranks if r != quad_rank])
            return 7, [quad_rank, kicker]
        
        elif count_values[0] == 3 and count_values[1] == 2:
            triple_rank = most_common[0][0]
            pair_rank = most_common[1][0]
            return 6, [triple_rank, pair_rank]
        
        elif is_flush:
            return 5, ranks_sorted
        
        elif is_straight:
            return 4, [straight_high]
        
        elif count_values[0] == 3:
            triple_rank = most_common[0][0]
            kickers = sorted([r for r in ranks if r != triple_rank], reverse=True)[:2]
            return 3, [triple_rank] + kickers
        
        elif count_values[0] == 2 and count_values[1] == 2:
            pairs = sorted([r for r, cnt in most_common if cnt == 2], reverse=True)
            kicker = max([r for r in ranks if r not in pairs])
            return 2, pairs + [kicker]
        
        elif count_values[0] == 2:
            pair_rank = most_common[0][0]
            kickers = sorted([r for r in ranks if r != pair_rank], reverse=True)[:3]
            return 1, [pair_rank] + kickers
        
        else:
            return 0, ranks_sorted

    def compare_hands(
        self, 
        hand1_eval: tuple[int, list[int]], 
        hand2_eval: tuple[int, list[int]]
    ) -> int:
        hand_type1, ranks1 = hand1_eval
        hand_type2, ranks2 = hand2_eval
        
        if hand_type1 > hand_type2:
            return -1
        elif hand_type1 < hand_type2:
            return 1
        
        for r1, r2 in zip(ranks1, ranks2):
            if r1 > r2:
                return -1
            elif r1 < r2:
                return 1
        
        return 0

    def find_best_hand_index(self, all_hands: dict[str, list[int]]) -> int:
        evaluated_hands = {player: self.evaluate_five_card_hand(hand) for player, hand in all_hands.items()}
        
        items = list(evaluated_hands.items())
        best_player, best_eval = items[0]
        
        for player, eval in items[1:]:
            if self.compare_hands(eval, best_eval) == -1:
                best_player = player
                best_eval = eval
        
        return best_player

    def hand_type_to_string(self, hand_type: int) -> str:
        types = {
            0: "High Card",
            1: "One Pair",
            2: "Two Pair",
            3: "Three of a Kind",
            4: "Straight",
            5: "Flush",
            6: "Full House",
            7: "Four of a Kind",
            8: "Straight Flush",
            9: "Royal Flush"
        }
        return types.get(hand_type, "Unknown")