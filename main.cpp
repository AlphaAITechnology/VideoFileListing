#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/split.hpp>
#include <iostream>
#include <set>
#include <string>
#include <vector>

using namespace std::string_literals;

std::string sortable_name(std::string& ts_file_name) {
    std::vector<std::string> s_{};
    boost::algorithm::split(s_, ts_file_name, boost::is_any_of(std::set<char>{'_'}));

    std::vector<std::string> date_{};
    boost::algorithm::split(date_, s_[0], boost::is_any_of(std::set<char>{'-'}));
    std::vector<std::string> time_{};
    boost::algorithm::split(time_, s_[1], boost::is_any_of(std::set<char>{'-'}));

    std::vector<int> date__{};
    std::transform(date_.cbegin(), date_.cend(), std::back_inserter(date__),
                   [](const std::string& sr) { return std::stoi(sr); });
    std::vector<int> time__{};
    std::transform(time_.cbegin(), time_.cend(), std::back_inserter(time__),
                   [](const std::string& sr) { return std::stoi(sr); });

    std::string res_time = std::to_string((time__[0] * 3600) + (time__[1] * 60) + (time__[2]));
    std::string res_date = std::to_string(date__[2])
                               .append((date__[0] >= 10) ? std::to_string(date__[0])
                                                         : "0"s.append(std::to_string(date__[0])))
                               .append((date__[1] >= 10) ? std::to_string(date__[1])
                                                         : "0"s.append(std::to_string(date__[1])));

    res_time.insert(res_time.begin(), 5 - res_time.size(), '0');
    return res_date.append("_").append(res_time);
}


int main([[maybe_unused]] int argc, [[maybe_unused]] char const* argv[]) {
    std::string s{argv[1]};
    std::cout << sortable_name(s) << std::endl;

    return 0;
}
