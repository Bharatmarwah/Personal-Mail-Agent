package com.bharatmarwah.mail_tool_service.Model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class EmailSendRequest {
    private String to;
    private String subject;
    private String body;
}
