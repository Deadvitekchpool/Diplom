def collapse(df):
    indexes_to_drop = []
    i = 0
    new_cols = []
    while i < len(df.values[0]):
        frames_len = 0
        prev = int(df.columns[i])
        new_cols += [prev]
        for col in df.columns[i:]:
            if int(col) != prev:
                break
            i += 1
            frames_len += 1

        frames = [row[i - frames_len:i] for row in df.values]
        for ii, frame in enumerate(frames):
            df.iat[ii, i-frames_len] = sum(frame)
        indexes_to_drop += list(range(i - frames_len + 1, i))
    to_drop = [df.columns[ind] for ind in indexes_to_drop]
    df = df.drop(to_drop, axis=1)
    df.columns = new_cols
    return df
