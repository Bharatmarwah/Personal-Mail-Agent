package com.bharatmarwah.mail_tool_service.Controller;


import com.bharatmarwah.mail_tool_service.Model.EmailSendRequest;
import com.bharatmarwah.mail_tool_service.Service.EmailService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/email")
@RequiredArgsConstructor
public class EmailController {

    private final EmailService emailService;

    @PostMapping

    public ResponseEntity<?> sendEmail(@RequestBody EmailSendRequest sendRequest){

        String result = emailService.sendEmail(sendRequest);

        return ResponseEntity.status(HttpStatus.OK).body(
                Map.of(
                        "status", "success",
                        "message", result
                )
        );
    }


}
