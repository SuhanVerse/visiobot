#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;

class CppTelemetrySubscriber : public rclcpp::Node
{
public:
  CppTelemetrySubscriber() : Node("cpp_telemetry_sub")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "visiobot_status", 10, std::bind(&CppTelemetrySubscriber::listener_callback, this, _1));
  }

private:
  void listener_callback(const std_msgs::msg::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "Received Status: '%s'", msg.data.c_str());
  }
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CppTelemetrySubscriber>());
  rclcpp::shutdown();
  return 0;
}