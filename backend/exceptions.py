# not all exceptions r being utilized yet

# base
class ResumeAppError(Exception):
    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# corrupt, unsupported or unreadable
class FileValidationError(ResumeAppError):
    status_code = 400
    error_code = "invalid_file"

# ai determined file is not a resume
class NotAResumeError(ResumeAppError):
    status_code = 422
    error_code = "not_a_resume"

# all ai providers failed
class AIServiceError(ResumeAppError):
    status_code = 502
    error_code = "ai_service_error"

# failed to render file
class PDFGenerationError(ResumeAppError):
    status_code = 500
    error_code = "pdf_generation_failed"

# invalid job id
class JobNotFoundError(ResumeAppError):
    status_code = 404
    error_code = "job_not_found"

# job not finished processing
class JobNotReadyError(ResumeAppError):
    status_code = 400
    error_code = "job_not_ready"

# invalid credentials
class AuthError(ResumeAppError):
    status_code = 401
    error_code = "auth_error"