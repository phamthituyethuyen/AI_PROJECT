#!/bin/bash

# Tải dữ liệu về và khai báo biến cho tiện sử dụng
wget -O moviesFilm.csv https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv
mvie="moviesFilm.csv"

# 1. Sắp xếp các bộ phim theo ngày phát hành giảm dần rồi lưu ra một file mới
csvsort -c release_date -r $mvie > movieSortedByDate.csv

# 2. Lọc ra các bộ phim có đánh giá trung bình trên 7.5 rồi lưu ra một file mới
echo "Phim có đánh giá trên 7.5:"
csvgrep -c vote_average -r '^[7-9]\.[5-9]$|^[1-9][0-9]\.[0-9]+$' $mvie > movieAbove75.csv
# 3. Tìm ra phim nào có doanh thu cao nhất và doanh thu thấp nhất
echo "Phim có doanh thu cao nhất:"
csvsort -c revenue $mvie | csvcut -c original_title,revenue | tail -n 1
echo "Phim có doanh thu thấp nhất:"
min_revenue=$(csvsort -c revenue $mvie | csvcut -c revenue | head -n 1)
csvgrep -c revenue -r "^$min_revenue$" $mvie | csvcut -c original_title,revenue

# 4. Tính tổng doanh thu tất cả các bộ phim
echo "Tổng doanh thu của tất cả các bộ phim trong file là:"
csvcut -c revenue $mvie | csvstat --sum

# 5. Top 10 bộ phim đem về lợi nhuận cao nhất
mlr --csv put '$profits=$revenue - $budget' $mvie | csvcut -c original_title,profits | csvsort -c profits -r | head -n 10 > top_10_profit_movies.csv

# 6. Đạo diễn nào có nhiều bộ phim nhất và diễn viên nào đóng nhiều phim nhất
echo "Đạo diễn có nhiều phim nhất:"
awk -F, '{print $9}' $mvie | tr '|' '\n' | awk 'NF > 0' | sort | uniq -c | sort -n | tail -n 1
echo "Diễn viên có nhiều phim nhất:"
awk -F, '{print $7}' $mvie | tr '|' '\n' | awk 'NF > 0' | sort | uniq -c | sort -n | tail -n 1

# 7. Thống kê số lượng phim theo các thể loại
echo "Thống kê số lượng phim theo thể loại:"
csvcut -c genres $mvie | tail -n +2 | tr '|' '\n' | sort | uniq -c

# 8. Idea của bạn để có thêm những phân tích cho dữ liệu?
echo "Có thể phân tích thêm theo các tiêu chí như: top thể loại có doanh thu cao, mối quan hệ giữa ngân sách và doanh thu, hoặc so sánh giữa các năm về sự thay đổi trong các thể loại phim."
