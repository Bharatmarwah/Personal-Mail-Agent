package com.bharatmarwah.mail_tool_service.Controller;


import com.bharatmarwah.mail_tool_service.Model.EmailSendRequest;
import com.bharatmarwah.mail_tool_service.Service.EmailService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/email")
@RequiredArgsConstructor
public class EmailController {

    private final EmailService emailService;

    @PostMapping
    @ResponseStatus(HttpStatus.OK)
    public String sendEmail(@RequestBody EmailSendRequest sendRequest){
        return emailService.sendEmail(sendRequest);
    }


}
