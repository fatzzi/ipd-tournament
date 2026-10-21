def steady(last_moves, my_history, opponents_histories, meta):
    # Friendly tit-for-tat: start nice, copy the opponent, forgive now and then.
    if not last_moves:
        return 'C'
    if meta['n_players'] > 2:
        return 'C' if last_moves.count('C') * 2 >= len(last_moves) else 'D'
    if last_moves[0] == 'D' and meta['rng'].random() < 0.1:
        return 'C'
    return last_moves[0]
