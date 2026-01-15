from collections import Counter, defaultdict

class CardCheckService:
    def best_poker_hand(self, cards: list[int]) -> tuple[str, list[int], list[int]]:
        cards = sorted(cards, key=lambda c: c % 10, reverse=True)
        
        suits = defaultdict(list)
        ranks_counter = Counter()
        
        for card in cards:
            suit = card % 10
            rank = card // 10
            
            suits[suit].append(card)
            
            ranks_counter[rank] += 1
        
        flush_cards = None
        for suit_cards in suits.values():
            if len(suit_cards) >= 5:
                flush_cards = sorted(suit_cards, key=lambda c: c // 10, reverse=True)
                break
        
        if flush_cards:
            straight_flush_result = self._find_straight(flush_cards)
            if straight_flush_result:
                straight_flush_cards, high_rank = straight_flush_result
                if high_rank == 14:  
                    return "ROYAL FLUSH", straight_flush_cards, [10]
                return "STRAIGHT FLUSH", straight_flush_cards, [high_rank]
        
        quad_rank = None
        for rank, count in ranks_counter.most_common():
            if count == 4:
                quad_rank = rank
                break
        
        if quad_rank:
            quad_cards = [c for c in cards if c // 10 == quad_rank]
            kicker = max([c for c in cards if c // 10 != quad_rank], key=lambda c: c // 10)
            best_hand = quad_cards + [kicker]
            return "FOUR OF A KIND", best_hand, [quad_rank, kicker // 10]
        
        triples = []
        pairs = []
        
        for rank, count in ranks_counter.most_common():
            if count >= 3:
                triples.append(rank)
            if count >= 2:
                pairs.append(rank)

        pairs = [p for p in pairs if p not in triples or triples.count(p) < 2]
        
        if triples and len(pairs) + len(triples) >= 2:
            triples.sort(reverse=True)
            pairs.sort(reverse=True)
            
            best_triple = triples[0]
            
            if len(triples) >= 2:
                best_pair = triples[1]
            else:
                best_pair = pairs[0] if pairs else None
            
            if best_pair:
                triple_cards = [c for c in cards if c % 10 == best_triple][:3]
                pair_cards = [c for c in cards if c % 10 == best_pair][:2]
                best_hand = triple_cards + pair_cards
                return "FULL HOUSE", best_hand, [best_triple, best_pair]
        
        if flush_cards:
            return "FLUSH", flush_cards[:5], [c % 10 for c in flush_cards[:5]]
        
        unique_ranks = sorted(set(c % 10 for c in cards), reverse=True)
        straight_result = self._find_straight_in_ranks(unique_ranks)
        if straight_result:
            high_rank, straight_ranks = straight_result
            straight_cards = []
            for rank in straight_ranks:
                for card in cards:
                    if card % 10 == rank and card not in straight_cards:
                        straight_cards.append(card)
                        break
            return "STRAIGHT", straight_cards, [high_rank]
        
        if triples:
            best_triple = triples[0]
            triple_cards = [c for c in cards if c % 10 == best_triple][:3]
            kickers = [c for c in cards if c % 10 != best_triple]
            kickers = sorted(kickers, key=lambda c: c % 10, reverse=True)[:2]
            best_hand = triple_cards + kickers
            return "THREE OF A KIND", best_hand, [best_triple] + [k % 10 for k in kickers]
        
        if len(pairs) >= 2:
            pairs.sort(reverse=True)
            first_pair_rank = pairs[0]
            second_pair_rank = pairs[1]
            
            first_pair_cards = [c for c in cards if c % 10 == first_pair_rank][:2]
            second_pair_cards = [c for c in cards if c % 10 == second_pair_rank][:2]
            
            kickers = [c for c in cards if c % 10 not in (first_pair_rank, second_pair_rank)]
            kicker = max(kickers, key=lambda c: c % 10) if kickers else None
            
            best_hand = first_pair_cards + second_pair_cards
            if kicker:
                best_hand.append(kicker)
                return "TWO PAIR", best_hand, [first_pair_rank, second_pair_rank, kicker % 10]
            return "TWO PAIR", best_hand, [first_pair_rank, second_pair_rank]
        
        if pairs:
            pair_rank = pairs[0]
            pair_cards = [c for c in cards if c % 10 == pair_rank][:2]
            kickers = [c for c in cards if c % 10 != pair_rank]
            kickers = sorted(kickers, key=lambda c: c % 10, reverse=True)[:3]
            best_hand = pair_cards + kickers
            return "ONE PAIR", best_hand, [pair_rank] + [k % 10 for k in kickers]
        
        return "HIGH CARD", cards[:5], [c % 10 for c in cards[:5]]

    def _find_straight(self, cards: list[int]) -> tuple[list[int], int] | None:
        unique_ranks = sorted(set(c % 10 for c in cards), reverse=True)
        
        if set([14, 2, 3, 4, 5]).issubset(unique_ranks):
            straight_cards = []
            for rank in [5, 4, 3, 2, 14]: 
                for card in cards:
                    if card % 10 == rank and card not in straight_cards:
                        straight_cards.append(card)
                        break
            return straight_cards, 5  
        
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                current_ranks = unique_ranks[i:i + 5]
                if all(current_ranks[j] - current_ranks[j + 1] == 1 for j in range(4)):
                    straight_cards = []
                    for rank in current_ranks:
                        for card in cards:
                            if card % 10 == rank and card not in straight_cards:
                                straight_cards.append(card)
                                break
                    return straight_cards, current_ranks[0]
        
        return None

    def _find_straight_in_ranks(self, unique_ranks: list[int]) -> tuple[int, list[int]] | None:
        if set([14, 2, 3, 4, 5]).issubset(unique_ranks):
            return 5, [5, 4, 3, 2, 14] 
        
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                current_ranks = unique_ranks[i:i + 5]
                if all(current_ranks[j] - current_ranks[j + 1] == 1 for j in range(4)):
                    return current_ranks[0], current_ranks
        
        return None