using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace OmniServer
{
    public partial class MainWindow : Form
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        // Start
        private void button1_Click(object sender, EventArgs e)
        {
            if (this.checkBox1.Checked)
                this.consoleControl1.StartProcess("WebServer.exe", int.Parse(this.numericUpDown1.Value.ToString()).ToString() + " --debug");
            else
                this.consoleControl1.StartProcess("WebServer.exe", int.Parse(this.numericUpDown1.Value.ToString()).ToString());
            this.button1.Enabled = false;
            this.button2.Enabled = true;
            this.label2.Text = "STATUS: RUNNING";
        }

        // Stop
        private void button2_Click(object sender, EventArgs e)
        {
            this.consoleControl1.WriteInput("s", System.Drawing.Color.White, false);
            this.button1.Enabled = true;
            this.button2.Enabled = false;
            this.label2.Text = "STATUS: NOT RUNNING";
        }
    }
}
