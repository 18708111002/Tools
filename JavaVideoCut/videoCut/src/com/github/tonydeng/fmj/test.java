package com.github.tonydeng.fmj;
import com.github.tonydeng.fmj.model.VideoInfo;
import com.github.tonydeng.fmj.runner.FFmpegCommandRunner;
import it.sauronsoftware.jave.Encoder;
import it.sauronsoftware.jave.MultimediaInfo;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import com.google.common.collect.Lists;


public class test {

    private long ReadVideoTime(File source) {
        Encoder encoder = new Encoder();
//        String length = "";
        long len = 0;
        try {
            MultimediaInfo m = encoder.getInfo(source);
            len = m.getDuration()/1000;
//            int hour = (int) (ls/3600);
//            int minute = (int) (ls%3600)/60;
//            int second = (int) (ls-hour*3600-minute*60);
//            length = hour+"'"+minute+"''"+second+"'''";
        } catch (Exception e) {
            e.printStackTrace();
        }
        return len;
    }

    public static void  main(String argv[]) {

        File img = FFmpegCommandRunner.screenshot(new File("D:\\inputvideo\\八卦来了！闭关已久的唐嫣终于携新剧回归了，最后亮了.mp4"),8);

    }
}
