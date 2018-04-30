package com.github.tonydeng.fmj;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import javax.swing.JFileChooser;
import javax.swing.JList;
import javax.swing.BorderFactory;
import javax.swing.ListSelectionModel;
import javax.swing.JPanel;
import javax.swing.*;
import javax.swing.DefaultListModel;
import  javax.swing.JFrame;


class MyWindowDemo {
    private Frame f;
    private TextField tf;

    private Button but_open;
    private Button but_recut;
    private Button but_delete;

    private TextArea ta;
    private String[] videoFile;

    private static JList  fileList = null;

    MyWindowDemo() {
        init();
    }

    public void init() {

//        JPanel left_jPanel = new JPanel(new GridLayout(12,1));
//        JPanel right_jPanel = new JPanel(new GridLayout(12,1));
//        JPanel btn_jPanel = new JPanel(new FlowLayout());


        f = new Frame("截图");//创建窗体对象
        f.setBounds(300, 100, 600, 500);//设置窗体位置和大小
        f.setLayout(new GridLayout(1,2));

        BorderLayout layout = new BorderLayout();
        f.setLayout(layout);

//        tf = new TextField(60);//创建单行文本对象60长度大小字符

        but_open = new Button("打开文件");//创建按钮对象
        but_open.setBounds(0,0,100,100);
        but_recut = new Button("删除");//创建按钮对象
        but_recut.setBounds(101,0,100,100);
        but_delete = new Button("重新截图");//创建按钮对象
        but_delete.setBounds(201,0,100,100);
//        btn_jPanel.add(but_open);
//        btn_jPanel.add(but_recut);
//        btn_jPanel.add(but_delete);




        fileList = new JList();
        fileList.setBorder(BorderFactory.createTitledBorder("待处理文件"));
        fileList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        fileList.setBounds(400, 400, 100, 200);
//        fileList.setSize(400,500);
//        left_jPanel.add(btn_jPanel,BorderLayout.NORTH);
//        left_jPanel.add(fileList,BorderLayout.SOUTH);

//        f.add(tf);//单行文本添加到窗体上
//        f.add(left_jPanel,BorderLayout.WEST);//按钮添加到窗体上
//        f.add(right_jPanel,BorderLayout.EAST);
//        f.add(ta);//多行文本添加到窗体上
//        f.add(fileList,BorderLayout.WEST);
        f.add(but_open);
        f.add(but_delete);
        f.add(but_recut);
        f.add(fileList);

        myEvent();//加载事件处理

        f.setExtendedState(f.getExtendedState() | JFrame.MAXIMIZED_BOTH);//全屏打开
        f.setVisible(true);//设置窗体可见

    }

    private void myEvent() {

        //按钮事件监听器
        but_open.addActionListener(new ActionListener()
        {

            public void actionPerformed(ActionEvent e) {

                JFileChooser fc = new  JFileChooser("d:\\inputvideo");
                fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);//设置只能选择目录
                fc.showOpenDialog(null);
                File f = fc.getSelectedFile();
                System.out.print(f.getAbsolutePath());
                String dirPath = f.getAbsolutePath();//获取单行文本内容保存到字符串dirPath中
                File dir=new File(dirPath);//将字符串dirPath封装成文件

                //如果文件存在，而且是个目录执行下列操作
                if(dir.exists() &&dir.isDirectory())
                {
                    videoFile =dir.list();//文件目录列表存放到字符数组中
                    fileList.setListData(videoFile);

                }


            }


        });
        //窗体关闭监听器
        f.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);

            }

        });

    }
    public static void main(String[] args){

        new MyWindowDemo();
    }

}