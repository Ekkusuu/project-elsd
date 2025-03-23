

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
timeline history {
    title = "World Wars Timeline";

    event ww1 {
        title = "World War I begins";
        date = 1914;
        importance = high;
    };

    event ww2 {
        title = "World War II begins";
        date = 1939;
        importance = high;
    };

    period cold_war {
        title = "Cold War";
        start = 1947;
        end = 1991;
        importance = medium;
    };

    relationship ww1_ww2 {
        from = ww1;
        to = ww2;
        type = cause-effect;
    };

    export history;
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

## **Grammar**  

### **Lexical Rules**  
- **Keywords:** `event`, `period`, `timeline`, `relationship`, `export`, `if`, `else`, `for`, `in`, `BCE`, `CE`, etc.  
- **Comments:** Start with `//` and extend to the end of the line  
- **Identifiers:** Must start with an alphabetic character or `_`, followed by alphanumeric characters  
- **String Literals:** Enclosed in double quotes (`" "`)  

### **Grammar Rules (Simplified)**  
```antlr
grammar TimelineDSL;

program: declaration* main_block?;

declaration: event_decl | period_decl | timeline_decl | relationship_decl;

event_decl: 'event' ID '{' 'title' '=' STRING ';' 'date' '=' date_expr ';' ('importance' '=' importance_value ';')? '}' ';';

period_decl: 'period' ID '{' 'title' '=' STRING ';' 'start' '=' date_expr ';' 'end' '=' date_expr ';' ('importance' '=' importance_value ';')? '}' ';';

timeline_decl: 'timeline' ID '{' 'title' '=' STRING ';' component_list '}' ';';

relationship_decl: 'relationship' ID '{' 'from' '=' ID ';' 'to' '=' ID ';' 'type' '=' relationship_type ';' '}' ';';

date_expr: YEAR_LITERAL | MONTH_YEAR_LITERAL | FULL_DATE_LITERAL | date_calculation;

date_calculation: ID '.' ('year' | 'month' | 'day') ('+' | '-') INT_LITERAL;

main_block: 'main' '{' statement* '}' ';';
```

