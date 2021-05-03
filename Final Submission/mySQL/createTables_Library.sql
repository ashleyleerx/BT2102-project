CREATE TABLE MemberUser(  
     memberID    		VARCHAR(25)    NOT NULL,
     memberPassword		VARCHAR(25)    NOT NULL,
	 PRIMARY KEY (memberID)); 
     
CREATE TABLE AdminUser(  
     adminID    		VARCHAR(25)    NOT NULL,
     adminPassword      VARCHAR(25)    NOT NULL,
	 PRIMARY KEY (adminID)); 

CREATE TABLE Book(  
     bookID    			INT			   NOT NULL,
     bookTitle      	VARCHAR(40),
     borrowMemberID     VARCHAR(25),
     reserveMemberID    VARCHAR(25),
     dateDue    		DATE,
	 PRIMARY KEY (bookID),
     FOREIGN KEY (borrowMemberID)     REFERENCES MemberUser(memberID) ON DELETE NO ACTION
                                                           ON UPDATE CASCADE,
	 FOREIGN KEY (reserveMemberID)    REFERENCES MemberUser(memberID) ON DELETE NO ACTION
                                                           ON UPDATE CASCADE);                                                          

CREATE TABLE Payment(  
     memberID    		VARCHAR(25)    NOT NULL,
     paymentAmount      INT   		   NOT NULL,
     paymentDate 		DATE           NOT NULL,
	 PRIMARY KEY (memberID, paymentDate),
	 FOREIGN KEY (memberID)    REFERENCES MemberUser(memberID) ON DELETE NO ACTION
                                                           ON UPDATE CASCADE); 

                                                           
CREATE TABLE Fine(  
     memberID    		VARCHAR(25)		NOT NULL,		
     fineAmount      	INT   		   	NOT NULL,
     paymentDate 		DATE, 			
     fineDate 			DATE  		   	NOT NULL, 
	 PRIMARY KEY (memberID, fineDate),
	 FOREIGN KEY (memberID)    REFERENCES MemberUser(memberID) ON DELETE NO ACTION
                                                           ON UPDATE CASCADE,
	 FOREIGN KEY (memberID, paymentDate)   	REFERENCES Payment(memberID, paymentDate) ON DELETE NO ACTION
                                                           ON UPDATE CASCADE);                                                          
                                                           
                                                            
                                                           