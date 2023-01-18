


import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
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

class CodeField extends JTextArea{
    Font fieldFont = new Font("Consolas", Font.PLAIN, 16);
    int fontSize = 20;
    CodeField(){
        setBackground(Color.LIGHT_GRAY);
        setFont(fieldFont);
    }
    void increaseFont(){
        fieldFont = fieldFont.deriveFont(++fontSize);

    }
    void decreaseFont(){
        fieldFont.deriveFont(--fontSize);
    }




}

class DocumentationAndExample{

    String title;
    String codeExample;
    String information;

}
public class Main {
    static String currentCode;

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
        runButton.setBounds(500,10,80,20);;
        runButton.setBackground(Color.GREEN);
        runButton.setOpaque(true);
        runButton.setBorderPainted(false);
        CodeField codeInputField = new CodeField();
        codeInputField.setText(currentCode);
        codeInputField.setBounds(50,50,500,500);
        JLabel savingLabel = new JLabel("Feel free to switch between this tab and the documentation. Your work will be saved!");
        savingLabel.setBounds(100,600,600,40);

        DescriptionField outputField = new DescriptionField();
        outputField.setBounds(600,50,500,500);
        inputOutputPanel.add(savingLabel);
        inputOutputPanel.add(runButton);
        inputOutputPanel.add(outputField);
        inputOutputPanel.add(codeInputField);
        displaySideBar(sideBarPanel, inputOutputPanel, codeInputField);
        panel.add(inputOutputPanel);
        panel.add(sideBarPanel);


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
                currentCode = field.getText();
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