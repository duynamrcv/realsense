#include <librealsense2/rs.hpp>

#include <opencv2/opencv.hpp>
#include <opencv2/rgbd.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui/highgui_c.h>

using namespace cv;

// return depth map that apply colormap
void colorDepthMap(const Mat& depth_raw, const int& color_map, Mat& depth_show)
{
    depth_show = Mat(depth_raw.size(), CV_8U);
    depth_raw.convertTo(depth_show, CV_8U, 255.0/65535);
    convertScaleAbs(depth_show, depth_show, 8.0);
    applyColorMap(depth_show, depth_show, color_map);
    return;
}

void depthCleaner(Mat& clean_depth)
{
    const unsigned char no_depth = 0;
    Mat temp1, temp2;
    Mat small_depthf;

    resize(clean_depth, small_depthf, clean_depth.size(), 1, 1);

    // inpaint only the masked "unknown" pixel
    inpaint(small_depthf, (small_depthf == no_depth), temp1, 5.0, INPAINT_TELEA);

    resize(temp1, temp2, temp1.size());
    temp2.copyTo(clean_depth, (clean_depth == no_depth));
    return;
}

int main()
{
    // config depth
    rs2::pipeline pipeline;
    rs2::config config;

    const int w = 640;
    const int h = 480;

    config.enable_stream(RS2_STREAM_DEPTH, w, h, RS2_FORMAT_Z16, 30);
    
    // start stream
    pipeline.start(config);

    // create a depth cleaner instance
    rgbd::DepthCleaner* depthc = new rgbd::DepthCleaner(
                CV_16U, 7, rgbd::DepthCleaner::DEPTH_CLEANER_NIL);

    while(true)
    {   
        // wait for frames
        rs2::frameset frames = pipeline.wait_for_frames();
        rs2::frame depth_frame = frames.get_depth_frame();
        if(!depth_frame) continue;

        // convert to Mat
        Mat depth_img(Size(w, h), CV_16UC1, (void*)depth_frame.get_data(), Mat::AUTO_STEP);
       
        // initialize clean depth
        Mat clean_img(depth_img.size(), CV_16U);

        // cleaner depth instance
        depthc->operator()(depth_img, clean_img);

        depthCleaner(clean_img);

        // visualize
        Mat depth_show, clean_show;
        colorDepthMap(depth_img, COLORMAP_JET, depth_show);
        colorDepthMap(clean_img, COLORMAP_JET, clean_show);
        
        Mat show_img;
        hconcat(depth_show, clean_show, show_img);
        imshow("", show_img);
        waitKey(1);
    }
    pipeline.stop();
    return 0;
}