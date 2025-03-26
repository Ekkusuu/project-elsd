

# **Timeline DSL**  

## **Overview**  
Timeline DSL is a **domain-specific language** designed to simplify the **creation, customization, and visualization of timelines**. It allows users to define historical events, periods, and relationships efficiently with a structured syntax.  


## **Key Features**  
✔ **Define Events & Periods** – Easily specify historical events and time periods  
✔ **Relationships** – Model cause-effect, precedes, follows, and contemporaneous relationships  
✔ **Control Structures** – Use `if`, `else`, and `for` loops to manipulate timeline data  
✔ **Customizable Styling** – Modify colors, markers, and text for better visualization  
✔ **Flexible Date Formats** – Support for BCE/CE, full dates, and relative calculations  
✔ **Export Timelines** – Compile and export timelines for integration into reports  

---

## **DSL Syntax**  

### **Example Timeline DSL Script**  
```dsl
// Define events
event juliusCaesarBirth {
    title = "Birth of Julius Caesar";
    date = 12-07-100 BCE;
    importance = medium;
};

event juliusCaesarDeath {
    title = "Assassination of Julius Caesar";
    date = 15-03-44 BCE;
    importance = high;
};

event augustusEmpire {
    title = "Augustus becomes first Roman Emperor";
    date = 27 BCE;
    importance = high;
};

event romanEmpireFall {
    title = "Fall of Western Roman Empire";
    date = 476 CE;
    importance = high;
};

// Define periods
period romanRepublic {
    title = "Roman Republic";
    start = 509 BCE;
    end = 27 BCE;
    importance = high;
};

period romanEmpire {
    title = "Roman Empire";
    start = 27 BCE;
    end = 476 CE;
    importance = high;
};

period juliusCaesarLife {
    title = "Life of Julius Caesar";
    start = 100 BCE;
    end = 44 BCE;
    importance = medium;
};

// Define relationships
relationship caesarRepublic {
    from = juliusCaesarDeath;
    to = romanRepublic;
    type = "contributed to end";
};

relationship augustusStartsEmpire {
    from = augustusEmpire;
    to = romanEmpire;
    type = cause-effect;
};

// Create timeline
timeline romanHistory {
    title = "Roman History";
    juliusCaesarBirth, juliusCaesarDeath, augustusEmpire, romanEmpireFall,
    romanRepublic, romanEmpire, juliusCaesarLife;
};

// Main program
main {
    // Find all events in the first century BCE and increase their importance
    for item in romanHistory {
        if (item.date.year < 0) {
            modify item {
                importance = high;
            };
        }
    };

    // Compile and export the timeline
    export romanHistory;
};

```

### **Supported Date Formats**  
- **Year only:** `1945`, `356 BCE`  
- **Month-Year:** `05-1945 CE`, `03-44 BCE`  
- **Full Date:** `08-05-1945 CE`, `15-03-44 BCE`  
- **Relative Date Calculation:**  
  ```dsl
  event discovery {
      title = "Scientific Discovery";
      date = ww1.date + 10;
  };
  ```

---

## **Lexical Rules**  

### **Keywords:**
- `event`, `period`, `timeline`, `relationship`, `main`, `export`, `if`, `else`, `for`, `in`, `modify`  
- Relationship types: `cause-effect`, `contemporaneous`, `precedes`, `follows`, `includes`, `excludes`  
- Importance levels: `high`, `medium`, `low`  
- Date notations: `BCE`, `CE`

### **Identifiers:**  
Identifiers must start with an alphabetic character or underscore and can be followed by alphanumeric characters or underscores.  

### **Strings:**  
Strings are enclosed in double quotes, and escape sequences like `\"`, `\\`, `\n`, and `\t` are supported.  

### **Date Formats:**  
- **Year:** `1945`, `356 BCE`
- **Month-Year:** `05-1945 CE`, `03-44 BCE`
- **Full Date:** `08-05-1945 CE`, `15-03-44 BCE`
- **Date Calculation:** Can perform calculations like `ww1.date + 10`.

### **Operators & Punctuation:**  
- **Comparison Operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Arithmetic Operators:** `+`, `-`
- **Punctuation:** `=`, `,`, `;`, `.`, `(`, `)`, `{`, `}`, `-`  

### **Boolean Literals:**  
- `true`, `false`

### **Numeric Literals:**  
- **Integer:** Any sequence of digits (e.g., `123`, `456`)
  
---

### **Grammar Rules**  
```antlr
parser grammar TimelineParser;
options { tokenVocab=TimelineLexer; }

program: declaration* mainBlock? EOF;

declaration: eventDecl | periodDecl | timelineDecl | relationshipDecl;

eventDecl: EVENT ID LCURLY TITLE EQ STRING SEMI DATE EQ dateExpr SEMI (IMPORTANCE EQ importanceValue SEMI)? RCURLY SEMI;

periodDecl: PERIOD ID LCURLY TITLE EQ STRING SEMI START EQ dateExpr SEMI END EQ dateExpr SEMI (IMPORTANCE EQ importanceValue SEMI)? RCURLY SEMI;

timelineDecl: TIMELINE ID LCURLY TITLE EQ STRING SEMI componentList SEMI RCURLY SEMI;

componentList: ID (COMMA ID)* SEMI;

relationshipDecl: RELATIONSHIP ID LCURLY FROM EQ ID SEMI TO EQ ID SEMI TYPE EQ relationshipType SEMI RCURLY SEMI;

dateExpr: fullDateLiteral | monthYearLiteral | yearLiteral | dateCalculation;

dateCalculation: ID DOT (YEAR | MONTH | DAY) ADD_OP INT;

yearLiteral: INT (BCE | CE)?;

monthYearLiteral: INT DASH yearLiteral;

fullDateLiteral: INT DASH monthYearLiteral;

importanceValue: HIGH | MEDIUM | LOW;

relationshipType: CAUSE_EFFECT | CONTEMPORANEOUS | PRECEDES | FOLLOWS | INCLUDES | EXCLUDES | STRING;

mainBlock: MAIN LCURLY statement* RCURLY SEMI;

statement: exportStmt | ifStmt | forStmt | modifyStmt | SEMI;

exportStmt: EXPORT ID SEMI;

ifStmt: IF LPAREN condition RPAREN LCURLY statement* RCURLY (ELSE LCURLY statement* RCURLY)?;

condition: expr comparisonOp expr | ID | booleanLiteral;

comparisonOp: EQ_EQ | NEQ | LT | GT | LE | GE;

expr: ID | STRING | dateExpr | INT | ID DOT property | importanceValue;

property: TITLE | DATE | START | END | IMPORTANCE | TYPE | YEAR | MONTH | DAY;

forStmt: FOR ID IN ID LCURLY statement* RCURLY SEMI;

modifyStmt: MODIFY ID LCURLY propertyAssignment+ RCURLY SEMI;

propertyAssignment: property EQ expr SEMI;

booleanLiteral: TRUE | FALSE;
```
