import operator

mingap, maxgap = 0.94, 1.06
trading_range = 1.1


def optimize_levels(chart, merge_levels=None):
    """Define variables"""
    candles = chart.candles
    lines = chart.levels
    if merge_levels != None:
        for k,v in merge_levels.items():
            lines[k] = v

    """
    Cluster lines which are near each other. 
    - store (date,price) for each level in cluster
    - return list groups ([]) with dicts of clusters ( {date:level} )
    """

    def cluster(lines):
        groups = []
        inGroup = False

        # Iter through initial lines
        for date, price in lines.items():
            i = list(lines.keys()).index(date)

            # if first iter, create new cluster
            if i == 0:
                groups.append({date: price})
            else:
                # get max/min/median of current group
                current_group = groups[-1]
                max_price = max(current_group.values())
                min_price = min(current_group.values())
                median_price = (max_price + min_price) / 2
                # if price is within max/min * median of group, add to group
                if median_price * maxgap > price > median_price * mingap:
                    groups[-1][date] = price
                else:
                    # create new group
                    groups.append({date: price})
        return groups

    """Filter levels with cluster()"""
    clustered_levels = cluster(lines)  # WAS SELF.LEVELS
    refined_levels = {}

    """Filter clustered levels"""
    for cluster in clustered_levels:

        # Set initial values which no stock could possibly have (?)
        initial_max_level = max(cluster.values())
        initial_min_level = min(cluster.values())
        max_level = initial_max_level
        min_level = initial_min_level
        start_date = list(cluster.keys())[0]
        end_date = list(cluster.keys())[-1]

        # if there are closes within the cluster that exceed range, add the extremes as lines
        for candle in candles:  # WAS SELF.CCANDLES
            if start_date.timestamp() < candle.date.timestamp() < end_date.timestamp():
                if candle.close > max_level or candle.open > max_level:
                    if candle.open > candle.close:
                        max_level = candle.open
                    else:
                        max_level = candle.close
                elif candle.close < min_level or candle.open < min_level:
                    if candle.close < candle.open:
                        min_level = candle.close
                    else:
                        min_level = candle.open

        if max_level > initial_max_level:
            refined_levels[start_date] = max_level
        else:
            refined_levels[start_date] = initial_max_level

        if min_level < initial_min_level:
            refined_levels[start_date] = min_level
        else:
            refined_levels[start_date] = initial_min_level
    #
    # for close in self.getData(timeframe='1mo')['Close']:
    #     refined_levels.append(close)

    """Final max/min optimization for groups"""
    sorted_levels = dict(sorted(refined_levels.items(), key=operator.itemgetter(1)))
    previous_level = 0
    optimized_levels = {}

    for date, level in sorted_levels.items():
        if previous_level == 0:
            optimized_levels[date] = level
            previous_level = level
        elif level > previous_level * trading_range:
            optimized_levels[date] = level
            previous_level = level

    return optimized_levels
