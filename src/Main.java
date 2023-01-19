


import javax.swing.*;
import javax.swing.event.ChangeListener;
import javax.swing.text.BadLocationException;
import javax.swing.text.Caret;
import javax.swing.text.DefaultCaret;
import javax.swing.text.JTextComponent;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;

class DescriptionField extends JTextArea{
    Font fieldFont = new Font("Serif", Font.PLAIN, 18);
    int fontSize=14;
    DescriptionField(){
        setBackground(Color.WHITE);
        setEditable(false);
        setFont(fieldFont);
        setLineWrap(true);
        setWrapStyleWord(true);

    }



}
class FancyCaret extends DefaultCaret {

    protected synchronized void damage(Rectangle r) {
        if (r == null)
            return;

        // give values to x,y,width,height (inherited from java.awt.Rectangle)
        x = r.x;
        y = r.y;
        height = r.height;
        // A value for width was probably set by paint(), which we leave alone.
        // But the first call to damage() precedes the first call to paint(), so
        // in this case we must be prepared to set a valid width, or else
        // paint()
        // will receive a bogus clip area and caret will not get drawn properly.
        if (width <= 0)
            width = getComponent().getWidth();

        repaint(); // calls getComponent().repaint(x, y, width, height)
    }

    public void paint(Graphics g) {
        JTextComponent comp = getComponent();
        if (comp == null)
            return;

        int dot = getDot();
        Rectangle r = null;
        char dotChar;
        try {
            r = comp.modelToView(dot);
            if (r == null)
                return;
            dotChar = comp.getText(dot, 1).charAt(0);
        } catch (BadLocationException e) {
            return;
        }

        if ((x != r.x) || (y != r.y)) {
            // paint() has been called directly, without a previous call to
            // damage(), so do some cleanup. (This happens, for example, when
            // the
            // text component is resized.)
            repaint(); // erase previous location of caret
            x = r.x; // Update dimensions (width gets set later in this method)
            y = r.y;
            height = r.height;
        }

        g.setColor(Color.WHITE);
        g.setXORMode(comp.getBackground()); // do this to draw in XOR mode

        if (dotChar == '\n') {
            int diam = r.height;
            if (isVisible())
                g.fillArc(r.x - diam / 2, r.y, diam, diam, 270, 180); // half
            // circle
            width = diam / 2 + 2;
            return;
        }

        if (dotChar == '\t')
            try {
                Rectangle nextr = comp.modelToView(dot + 1);
                if ((r.y == nextr.y) && (r.x < nextr.x)) {
                    width = nextr.x - r.x;
                    if (isVisible())
                        g.fillRoundRect(r.x, r.y, width, r.height, 12, 12);
                    return;
                } else
                    dotChar = ' ';
            } catch (BadLocationException e) {
                dotChar = ' ';
            }

        width = g.getFontMetrics().charWidth(dotChar);
        if (isVisible())
            g.fillRect(r.x, r.y, width, r.height);
    }}

class CodeField extends JTextArea implements KeyListener {
    Font fieldFont = new Font("Consolas", Font.PLAIN, 16);
    int fontSize = 20;





    CodeField(){
        setBackground(Color.BLACK);
        setForeground(Color.WHITE);
        setFont(fieldFont);
        setCaret(new FancyCaret());
    }
    void increaseFont(){
        fieldFont = fieldFont.deriveFont(++fontSize);

    }
    void decreaseFont(){
        fieldFont.deriveFont(--fontSize);
    }


    @Override
    public void keyTyped(KeyEvent keyEvent) {

    }

    @Override
    public void keyPressed(KeyEvent keyEvent) {

    }

    @Override
    public void keyReleased(KeyEvent keyEvent) {

    }
}

class DocumentationAndExample{

    String title;
    String codeExample;
    String information;
}
public class Main {
    static String currentCommand = "";
    static int currPos = 0;

    static String currentCode;
    static String currentOutput;
    static boolean firsTimeSetup = true;

    //global hashmap containing information about documentation and examples
    static HashMap<String, DocumentationAndExample> documentationDatabase = new HashMap<>();

    public static void main(String[] args) {
        startProgram();
    }
    public static void initHashMap(){
        DocumentationAndExample varDoc = new DocumentationAndExample();
        varDoc.codeExample = "#delare a variable of type int like this \nint testVariable = 14;\n" +
                "#you can modify the value of a declared variable like \n" +
                "testVariable = 12;  #the value of this variable will now be 12 \n" +
                "#you may assign a boolean variable like this\n" +
                "bool myBoolean = True;   #you are also able to modify the value the same way\n" +
                "myBoolean = False";
        varDoc.title = "Variable declaration";
        varDoc.information = "You may declare a variable in bos by using the syntax type identifier = value;\n" +
                "Possible types include int, bool, char, and string\n" +
                "Redeclaration looks like identifier = newvalue";

        documentationDatabase.put("var declaration", varDoc);
        DocumentationAndExample loopDoc = new DocumentationAndExample();
        loopDoc.codeExample = "#start a for loop like this\n" +
                "#first declare a variable\n" +
                "int i =5;\n" +
                "int g=10"+
                "for(i; i<10; ++i) ++g\n"+
                "#g will be incremented 5 times\n\n\n" +
                "#to declare a while loop, we must have a condition\n" +
                "bool condition = True\n" +

                "while(condition) ++g\n" +
                "#g will be incremented forever\n";
        loopDoc.information = "For loops are declared a bit differently in bos than in other languages\n" +
                "We must FIRST declare a variable to use inside the for loop and then in first argument of the for loop we must " +
                "specify the variable. In the next argument we must specify a condition and in the third we must give an increment " +
                "operation. \n" +
                "VERY IMPORTANT: in bos, you can ONLY increment by doing ++variable and doing variable++ will NOT work";
        loopDoc.title = "For and while loops";
        documentationDatabase.put("loops", loopDoc);
        DocumentationAndExample statementsDoc = new DocumentationAndExample();
        statementsDoc.codeExample = "#to make an if statement, the syntax resembles many other languages:\n" +
                "int g =2;\n" +

                "if(True or False) ++g\n" +
                "#g will equal 3\n" +
                "if(True and False) ++g\n" +
                "#g will still equal 3";
        statementsDoc.information = "An if statement is declared as such: \n" +
                "if(condition) expression\n" +
                "you may also use elif (meaning else if) or else statements to account for multiple cases\n" +
                "if(condition_1) expression_1 elif(condition_2) expression_2 elif(condition_3) expression_3 else expression_4";
        statementsDoc.title = "If, elif, and else statements";
        documentationDatabase.put("if statements", statementsDoc);
        DocumentationAndExample booleanOperations = new DocumentationAndExample();
        booleanOperations.information = "The bos language supports several different boolean operations.\n" +
                "Some of which include, 'and', 'or', '==', '!=', and 'xor'\n" +
                "You are able to use them in if statements, while conditions, for conditions or just on their own\n";
        booleanOperations.codeExample = "#you may use them in a variable declaration\n" +
                "bool my_boolean = True or False #evaluates to True\n" +
                "#you may use them in if statements\n" +
                "if(my_boolean !=False) 'test' #prints test\n";
        booleanOperations.title = "Boolean operations";
        documentationDatabase.put("boolean operations", booleanOperations);

        DocumentationAndExample commentingInformation =  new DocumentationAndExample();
        commentingInformation.information = "You may leave a comment on a single line using the # character\n" +
                "multi-line comments are currently not yet implemented\n" +
                "You are able to use more than one # if you wish to do so to create a single line comment";
        commentingInformation.codeExample = "bool my_bool = true;\n" +
                "#here is an example of a comment\n" +
                "#here is another comment\n" +
                "int my_number = 15; #you may also comment like this";
        commentingInformation.title= "Commenting";
        documentationDatabase.put("commenting", commentingInformation);
        DocumentationAndExample functionsInformation = new DocumentationAndExample();
        functionsInformation.information = "Feature is coming soon";
        functionsInformation.codeExample = "#coming soon";
        functionsInformation.title = "Functions";
        documentationDatabase.put("functions", functionsInformation);
        DocumentationAndExample listsInformation = new DocumentationAndExample();
        listsInformation.information = "You may declare a list in bos using square brackets and commas.\n" +
                "You may add new items to a list using the plus operator\n" +
                "You may also assign a list to a variable but use the keyword type of the list elements";
        listsInformation.codeExample = "int my_list = [1,2,3,4]\n" +
                "my_list+5 # returns [1,2,3,4,5]";
        listsInformation.title= "Lists";
        documentationDatabase.put("lists", listsInformation);
        DocumentationAndExample printInformation = new DocumentationAndExample();
        printInformation.information = "In bos, there is no specified print keyword that will print something to the screen\n" +
                "Instead, anytime you specify a type of perform an operation the value of it will be printed";
        printInformation.codeExample= "4+4 #prints 8\n" +
                "int i =5 #prints the value of as well as assigning;\n" +
                "++i #increments i but also prints the updated value\n" +
                "while(i<20) ++i #a list of all of i's values will be printed";
        printInformation.title = "Printing";
        documentationDatabase.put("printing", listsInformation);




    }
    public static void startProgram(){
        initHashMap();
        JFrame frame = new JFrame("Bos language");
        frame.setSize(1280,720);

        JPanel panel = new JPanel(null);
        codeWindow(panel);






        frame.setVisible(true);
        frame.add(panel);



    }
    public static void codeWindow(JPanel panel){
        panel.removeAll();
        JPanel inputOutputPanel = new JPanel(null);
        inputOutputPanel.setBounds(200,0,1080,720);

        panel.setBounds(0,0,1280,720);
        JPanel sideBarPanel = new JPanel(null);
        sideBarPanel.setBounds(0,0,200,720);
        JButton runButton = new JButton("Run");
        runButton.setBackground(Color.GREEN);
        runButton.setOpaque(true);
        runButton.setBorderPainted(false);
        CodeField codeInputField = new CodeField();
        JScrollPane codePane = new JScrollPane(codeInputField);
        if(firsTimeSetup){ codeInputField.setText("bos shell>"); firsTimeSetup =false;}

            DescriptionField outputField = new DescriptionField();
        JScrollPane scrollpane = new JScrollPane(outputField);
        scrollpane.setBounds(600,50,500,500);
        JButton clearInput = new JButton("Clear");
        clearInput.setBounds(100,10,80,20);
        inputOutputPanel.add(clearInput);
        clearInput.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                codeInputField.setText("bos shell>");
                currPos =0;
            }
        });
        JButton clearOutput = new JButton("Clear");
        clearOutput.setBounds(700,10,80,20);
        inputOutputPanel.add(clearOutput);
        clearOutput.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                outputField.setText("");
                currentCode = "bos shell>";
            }
        });

        codeInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent keyEvent) {

            }

            @Override
            public void keyPressed(KeyEvent keyEvent) {
                if(keyEvent.getKeyCode() == KeyEvent.VK_ENTER){
                    currentCommand = codeInputField.getText().substring(currPos);

                    codeInputField.append("\nbos shell> ");
                    System.out.println(currPos);
                    currPos = codeInputField.getText().length();
                    System.out.println(currentCommand+" current command");
                    ProcessBuilder builder = new ProcessBuilder("python3", System.getProperty("user.dir")+"/src/shell.py", currentCommand);
                    StringBuilder totalOutput = new StringBuilder();
                    try{
                        Process process = builder.start();
                        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                        BufferedReader errorReader = new BufferedReader(new InputStreamReader((process.getErrorStream())));
                        String lines;
                        System.out.println("test");
                        while((lines = reader.readLine())!=null){
                            totalOutput.append(lines+"\n");
                            System.out.println(lines);

                        }
                        while(((lines = errorReader.readLine())!= null)){
                            System.out.println("error"+lines);
                        }
                        System.out.println(totalOutput);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                    outputField.append(totalOutput.toString());
                    currentCode = codeInputField.getText();
                    currentOutput = outputField.getText();
                    codeInputField.setCaretPosition(-1);

                }
                else{

                }
            }

            @Override
            public void keyReleased(KeyEvent keyEvent) {

            }
        });
        codeInputField.setText(currentCode);
        outputField.setText(currentOutput);

        codePane.setBounds(50,50,500,500);
        JLabel savingLabel = new JLabel("Feel free to switch between this tab and the documentation. Your work will be saved!");
        savingLabel.setBounds(100,600,600,40);




        inputOutputPanel.add(savingLabel);
        inputOutputPanel.add(runButton);
        inputOutputPanel.add(scrollpane);
        inputOutputPanel.add(codePane);
        displaySideBar(sideBarPanel, inputOutputPanel, codeInputField);
        panel.add(inputOutputPanel);
        panel.add(sideBarPanel);
        panel.repaint();
        panel.revalidate();

    }




    public static void displaySideBar(JPanel sidebarPanel, JPanel mainPanel, CodeField field){

        sidebarPanel.removeAll();


        JButton tryItButton = new JButton("Try it out!");
        JButton documentationButton = new JButton("Documentation");
        JButton examplesButton = new JButton("Examples");
        tryItButton.setBounds(0,30,200,100);
        documentationButton.setBounds(0,130,200,100);
        examplesButton.setBounds(0,230,200,100);
        tryItButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                codeWindow(mainPanel);
            }
        });
        documentationButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                displayDocumentation(mainPanel);
            }
        });

        //adding to panel
        sidebarPanel.add(tryItButton);
        sidebarPanel.add(documentationButton);



    }
    public static void viewExampleAndDocumentation(JPanel mainPanel, String type){
        mainPanel.removeAll();
        DocumentationAndExample currentDoc = documentationDatabase.get(type);
        JPanel informationPanel = new JPanel(null);
        informationPanel.setBounds(0,100,500,720);
        Font titleFont = new Font("Serif", Font.BOLD, 30);
        JPanel titlePanel= new JPanel(null);
        JLabel titleLabel = new JLabel(currentDoc.title,SwingConstants.CENTER);
        titleLabel.setFont(titleFont);
        titlePanel.setBounds(0,0,1000,100);
        titleLabel.setBounds(0,0,1000,100);
        titlePanel.add(titleLabel);
        JPanel codePanel = new JPanel(null);
        codePanel.setBounds(500,100,600,720);
        DescriptionField descriptionArea = new DescriptionField();
        JScrollPane scrollableDescArea = new JScrollPane(descriptionArea);
        descriptionArea.setText(currentDoc.information);
        scrollableDescArea.setBounds(0,0,500,720);
        CodeField codeArea = new CodeField();
        JScrollPane scrollableCode = new JScrollPane(codeArea);
        codeArea.setBounds(0,0,480,700);
        codeArea.setText(currentDoc.codeExample);

        scrollableCode.setBounds(0,0,500,720);
        codePanel.add(scrollableCode);
        informationPanel.add(scrollableDescArea);
        mainPanel.add(titlePanel);
        mainPanel.add(informationPanel);
        mainPanel.add(codePanel);
        mainPanel.repaint();
        mainPanel.revalidate();



    }
    public static void displayDocumentation(JPanel mainPanel){

        //clear panel
        mainPanel.removeAll();
        mainPanel.revalidate();
        mainPanel.repaint();




        //printing to the screen
        JButton variableDeclarationInformationButton = new JButton("Variable declaration");
        variableDeclarationInformationButton.setBounds(30,120,300,80);
        mainPanel.add(variableDeclarationInformationButton);
        variableDeclarationInformationButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "var declaration");

            }
        });

        //functions
        JButton functionsInformationButton = new JButton("Functions information");
        functionsInformationButton.setBounds(30,200,300,80);
        mainPanel.add(functionsInformationButton);
        functionsInformationButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "functions");

            }
        });

        //loops
        JButton loopsInformationButton = new JButton("Loops information");
        loopsInformationButton.setBounds(30,280,300,80);
        mainPanel.add(loopsInformationButton);
        loopsInformationButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "loops");

            }
        });

        //commenting
        JButton commentingInformationButton = new JButton("Commenting information");
        commentingInformationButton.setBounds(30,360,300,80);
        mainPanel.add(commentingInformationButton);
        commentingInformationButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "commenting");

            }
        });

        //if statements
        JButton ifStatementInformation = new JButton("If statements");
        ifStatementInformation.setBounds(30,440,300,80);
        mainPanel.add(ifStatementInformation);
        ifStatementInformation.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "if statements");

            }
        });
        //printing to the screen
        JButton booleanExpressions = new JButton("Boolean operations");
        booleanExpressions.setBounds(30,520,300,80);
        mainPanel.add(booleanExpressions);
        booleanExpressions.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "boolean operations");

            }
        });
        //printing to the screen
        JButton listsInformation = new JButton("Lists");
        listsInformation.setBounds(400,120,300,80);
        mainPanel.add(listsInformation);
        listsInformation.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "lists");

            }
        });
        //printing to the screen
        JButton printingButton = new JButton("Printing");
        printingButton.setBounds(400,200,300,80);
        mainPanel.add(printingButton);
        printingButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewExampleAndDocumentation(mainPanel, "printing");

            }
        });
    }
}