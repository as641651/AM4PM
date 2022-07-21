def get_trace_durations(event_table):
    """calculates duration of each case from event table"""
    dfs = event_table.drop_duplicates('case:concept:name', keep='first')[['case:concept:name', 'timestamp:start']]
    dfe = event_table.drop_duplicates('case:concept:name', keep='last')[['case:concept:name', 'timestamp:end']]
    dfm = dfs.merge(dfe, on='case:concept:name')
    dfm['case:duration'] = dfm.apply(lambda row: row['timestamp:end'] - row['timestamp:start'], axis=1)
    dfm = dfm.rename(columns={
        'timestamp:start': 'case:timestamp:start',
        'timestamp:end': 'case:timestamp:end',
    })
    return dfm