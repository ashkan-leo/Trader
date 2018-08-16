set -e SYM
set -e fileName
set -e startDate
set -e endDate

set -x SYM $argv[4]
set fileName $argv[1]
set startDate $argv[2]
set endDate $argv[3]
set outName "/Users/ashkanaleali/w/Trader/pytrader/portfolio/$fileName.$SYM.$startDate.$endDate.pickle"


zipline run -f $fileName --start $startDate --end $endDate -o $outName